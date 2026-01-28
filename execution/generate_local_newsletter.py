#!/usr/bin/env python3
"""
Ultimate Local Newsletter Generator

Fully automated local newsletter workflow that scrapes events from Instagram,
Facebook, and web aggregators, deduplicates them, and generates ready-to-publish
newsletters.

Based on Aniket Panjwani's local newsletter automation methodology.

Usage:
    # Full automation
    python3 execution/generate_local_newsletter.py \
        --location "Austin, TX" \
        --instagram "@do512,@austin_events" \
        --web-sources "https://do512.com/events" \
        --newsletter-name "Austin Weekly"
    
    # Step by step
    python3 execution/generate_local_newsletter.py --setup --location "Austin, TX"
    python3 execution/generate_local_newsletter.py --research --location "Austin, TX"
    python3 execution/generate_local_newsletter.py --write --location "Austin, TX"

Follows directive: directives/ultimate_local_newsletter.md
"""

import argparse
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import requests
except ImportError:
    print("Error: requests required. pip install requests")
    sys.exit(1)

try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False
    print("Warning: rapidfuzz not installed. Deduplication will use exact matching.")
    print("Install with: pip install rapidfuzz")

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class LocalNewsletterGenerator:
    """Generate local newsletters from multiple event sources"""

    DEFAULT_CATEGORIES = [
        "Featured Events",
        "Music & Nightlife",
        "Food & Drink",
        "Arts & Culture",
        "Sports & Fitness",
        "Family-Friendly",
        "Free Events",
        "Other"
    ]

    def __init__(self, **kwargs):
        self.location = kwargs.get("location", "")
        self.newsletter_name = kwargs.get("newsletter_name", f"{self.location} Weekly")
        self.days_ahead = kwargs.get("days", 7)
        
        # Source configurations
        self.instagram_handles = kwargs.get("instagram", [])
        self.web_sources = kwargs.get("web_sources", [])
        self.facebook_urls = kwargs.get("facebook_urls", [])
        
        # Template options
        self.template_style = kwargs.get("template", "weekly")
        
        # Setup paths
        location_slug = re.sub(r'[^a-zA-Z0-9]', '_', self.location.lower())
        self.base_dir = Path(f".tmp/local_newsletters/{location_slug}")
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_dir = Path("config")
        self.config_dir.mkdir(exist_ok=True)
        
        self.db_path = self.base_dir / "events.db"
        self.config_path = self.config_dir / f"local_newsletter_{location_slug}.yaml"
        
        # API keys
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.scrapecreators_key = os.getenv("SCRAPECREATORS_API_KEY")
        self.firecrawl_key = os.getenv("FIRECRAWL_API_KEY")
        self.perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        self.unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")
        
        # ConvertKit / Kit API
        self.convertkit_key = os.getenv("CONVERTKIT_API_KEY")
        
        # Header image cache
        self._header_image_url = None
        
        # Publishing options
        self.publish_to_convertkit = kwargs.get("publish", False)
        self.publish_status = kwargs.get("publish_status", "draft")  # draft or send
        
        # Initialize database
        self._init_database()

    def log(self, message: str, level: str = "INFO"):
        """Log with timestamp and level indicator"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = {
            "INFO": "ℹ️",
            "SUCCESS": "✅",
            "WARNING": "⚠️",
            "ERROR": "❌",
            "STEP": "📍"
        }.get(level, "")
        print(f"[{timestamp}] {prefix} {message}")

    def _init_database(self):
        """Initialize SQLite database for event storage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unique_key TEXT UNIQUE,
                title TEXT NOT NULL,
                description TEXT,
                date DATE,
                time TEXT,
                end_date DATE,
                venue TEXT,
                address TEXT,
                category TEXT,
                source TEXT,
                source_url TEXT,
                image_url TEXT,
                price TEXT,
                is_free BOOLEAN DEFAULT 0,
                is_featured BOOLEAN DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scraped_urls (
                url TEXT PRIMARY KEY,
                source TEXT,
                scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_date ON events(date)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_events_category ON events(category)
        """)
        
        conn.commit()
        conn.close()
        self.log(f"Database initialized: {self.db_path}", "SUCCESS")

    def _generate_unique_key(self, title: str, date: str, venue: str) -> str:
        """Generate unique key for event deduplication"""
        normalized = f"{title.lower().strip()}|{date}|{venue.lower().strip()}"
        return hashlib.md5(normalized.encode()).hexdigest()[:16]

    def _is_duplicate(self, title: str, date: str, venue: str) -> bool:
        """Check if event is a duplicate using fuzzy matching"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT title, date, venue FROM events 
            WHERE date = ? OR date BETWEEN date(?, '-1 day') AND date(?, '+1 day')
        """, (date, date, date))
        
        existing = cursor.fetchall()
        conn.close()
        
        for existing_title, existing_date, existing_venue in existing:
            if RAPIDFUZZ_AVAILABLE:
                title_score = fuzz.ratio(title.lower(), existing_title.lower())
                venue_score = fuzz.ratio(venue.lower(), existing_venue.lower()) if venue and existing_venue else 100
                
                if title_score > 85 and venue_score > 70:
                    return True
            else:
                if title.lower() == existing_title.lower():
                    return True
        
        return False

    def call_openrouter(self, prompt: str, max_tokens: int = 4000) -> Optional[str]:
        """Call OpenRouter API for AI generation"""
        if not self.openrouter_key:
            self.log("OPENROUTER_API_KEY not set", "ERROR")
            return None

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.openrouter_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "anthropic/claude-sonnet-4",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": max_tokens
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                self.log(f"OpenRouter error: {response.status_code}", "ERROR")
                return None
        except Exception as e:
            self.log(f"OpenRouter exception: {e}", "ERROR")
            return None

    def call_perplexity(self, query: str) -> Optional[str]:
        """Call Perplexity for local research"""
        if not self.perplexity_key:
            return None
        
        try:
            response = requests.post(
                "https://api.perplexity.ai/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.perplexity_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "sonar",
                    "messages": [{"role": "user", "content": query}]
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            self.log(f"Perplexity error: {response.status_code}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Perplexity exception: {e}", "ERROR")
            return None

    def get_header_image(self, query: str = None) -> Optional[str]:
        """Get a header image from Unsplash for the location"""
        if self._header_image_url:
            return self._header_image_url
            
        if not self.unsplash_key:
            self.log("UNSPLASH_ACCESS_KEY not set - using default header", "WARNING")
            return None
        
        search_query = query or f"{self.location.split(',')[0]} skyline cityscape"
        
        try:
            response = requests.get(
                "https://api.unsplash.com/search/photos",
                params={
                    "query": search_query,
                    "orientation": "landscape",
                    "per_page": 1
                },
                headers={"Authorization": f"Client-ID {self.unsplash_key}"},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("results"):
                    photo = data["results"][0]
                    # Use the regular size (1080px wide)
                    self._header_image_url = photo["urls"]["regular"]
                    photographer = photo["user"]["name"]
                    self.log(f"Header image by {photographer} from Unsplash", "SUCCESS")
                    return self._header_image_url
            else:
                self.log(f"Unsplash error: {response.status_code}", "WARNING")
        except Exception as e:
            self.log(f"Unsplash exception: {e}", "WARNING")
        
        return None

    def scrape_instagram(self, handle: str) -> List[Dict]:
        """Scrape Instagram profile for events using ScrapeCreators API"""
        if not self.scrapecreators_key:
            self.log("SCRAPECREATORS_API_KEY not set - skipping Instagram", "WARNING")
            return []
        
        self.log(f"Scraping Instagram: {handle}", "STEP")
        
        handle = handle.lstrip("@")
        events = []
        
        try:
            # Use the correct ScrapeCreators API endpoint for posts
            response = requests.get(
                "https://api.scrapecreators.com/v2/instagram/user/posts",
                params={"handle": handle},
                headers={"x-api-key": self.scrapecreators_key},
                timeout=60
            )
            
            if response.status_code != 200:
                self.log(f"ScrapeCreators posts error for {handle}: {response.status_code}", "WARNING")
                # Try fallback to profile endpoint which includes recent posts
                response = requests.get(
                    "https://api.scrapecreators.com/v1/instagram/profile",
                    params={"handle": handle},
                    headers={"x-api-key": self.scrapecreators_key},
                    timeout=60
                )
                
                if response.status_code != 200:
                    self.log(f"ScrapeCreators profile error for {handle}: {response.status_code}", "ERROR")
                    return []
                
                data = response.json()
                user_data = data.get("data", {}).get("user", {})
                posts = user_data.get("edge_owner_to_timeline_media", {}).get("edges", [])
                
                for edge in posts[:20]:
                    post = edge.get("node", {})
                    caption_edges = post.get("edge_media_to_caption", {}).get("edges", [])
                    caption = caption_edges[0].get("node", {}).get("text", "") if caption_edges else ""
                    
                    if not caption:
                        continue
                    
                    event = self._extract_event_from_caption(caption, handle)
                    if event:
                        event["source"] = f"instagram:{handle}"
                        shortcode = post.get("shortcode", "")
                        event["source_url"] = f"https://instagram.com/p/{shortcode}" if shortcode else ""
                        event["image_url"] = post.get("display_url", "")
                        events.append(event)
            else:
                data = response.json()
                posts = data.get("data", [])
                
                for post in posts[:20]:
                    caption = post.get("caption", "") or post.get("text", "")
                    if not caption:
                        continue
                    
                    event = self._extract_event_from_caption(caption, handle)
                    if event:
                        event["source"] = f"instagram:{handle}"
                        event["source_url"] = post.get("url", "") or post.get("permalink", "")
                        event["image_url"] = post.get("thumbnail_url", "") or post.get("display_url", "")
                        events.append(event)
            
            self.log(f"Found {len(events)} potential events from @{handle}", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error scraping {handle}: {e}", "ERROR")
        
        return events

    def _extract_event_from_caption(self, caption: str, source: str) -> Optional[Dict]:
        """Use AI to extract event details from Instagram caption"""
        prompt = f"""Extract event information from this Instagram caption if it describes an event.

CAPTION:
{caption[:2000]}

If this is about an event, return JSON:
{{
    "is_event": true,
    "title": "Event name",
    "description": "Brief description",
    "date": "YYYY-MM-DD or null if unclear",
    "time": "HH:MM or null",
    "venue": "Venue name or null",
    "address": "Address or null",
    "price": "Price info or null",
    "is_free": true/false,
    "category": "One of: Music & Nightlife, Food & Drink, Arts & Culture, Sports & Fitness, Family-Friendly, Other"
}}

If NOT an event (just regular content), return:
{{"is_event": false}}

Return ONLY valid JSON."""

        result = self.call_openrouter(prompt, max_tokens=500)
        
        if result:
            try:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    data = json.loads(json_match.group())
                    if data.get("is_event"):
                        return data
            except json.JSONDecodeError:
                pass
        
        return None

    def scrape_web_source(self, url: str) -> List[Dict]:
        """Scrape web aggregator for events using Firecrawl"""
        if not self.firecrawl_key:
            self.log("FIRECRAWL_API_KEY not set - using basic scraping", "WARNING")
            return self._basic_web_scrape(url)
        
        self.log(f"Scraping web source: {url}", "STEP")
        
        events = []
        
        try:
            # First, map the site to get event URLs
            map_response = requests.post(
                "https://api.firecrawl.dev/v1/map",
                headers={
                    "Authorization": f"Bearer {self.firecrawl_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "url": url,
                    "search": "event"
                },
                timeout=60
            )
            
            if map_response.status_code != 200:
                self.log(f"Firecrawl map error: {map_response.status_code}", "ERROR")
                return []
            
            map_data = map_response.json()
            event_urls = map_data.get("links", [])[:20]  # Limit to 20 URLs
            
            self.log(f"Found {len(event_urls)} event URLs to scrape", "INFO")
            
            # Scrape each event URL
            for event_url in event_urls:
                if self._is_url_scraped(event_url):
                    continue
                
                event = self._scrape_single_url(event_url)
                if event:
                    events.append(event)
                    self._mark_url_scraped(event_url, urlparse(url).netloc)
                
                time.sleep(0.5)  # Rate limiting
            
            self.log(f"Extracted {len(events)} events from {urlparse(url).netloc}", "SUCCESS")
            
        except Exception as e:
            self.log(f"Error scraping {url}: {e}", "ERROR")
        
        return events

    def _scrape_single_url(self, url: str) -> Optional[Dict]:
        """Scrape a single event URL"""
        try:
            response = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                headers={
                    "Authorization": f"Bearer {self.firecrawl_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "url": url,
                    "formats": ["markdown"]
                },
                timeout=30
            )
            
            if response.status_code != 200:
                return None
            
            data = response.json()
            markdown = data.get("data", {}).get("markdown", "")
            
            if not markdown:
                return None
            
            return self._extract_event_from_markdown(markdown, url)
            
        except Exception:
            return None

    def _extract_event_from_markdown(self, markdown: str, source_url: str) -> Optional[Dict]:
        """Extract event details from scraped markdown"""
        prompt = f"""Extract event information from this webpage content.

CONTENT:
{markdown[:3000]}

SOURCE URL: {source_url}

Return JSON:
{{
    "title": "Event name",
    "description": "Brief description (1-2 sentences)",
    "date": "YYYY-MM-DD",
    "time": "HH:MM or null",
    "end_date": "YYYY-MM-DD or null",
    "venue": "Venue name",
    "address": "Full address or null",
    "price": "Price info or 'Free'",
    "is_free": true/false,
    "category": "One of: Music & Nightlife, Food & Drink, Arts & Culture, Sports & Fitness, Family-Friendly, Other"
}}

Return ONLY valid JSON. If not enough info for an event, return {{"error": "not enough info"}}"""

        result = self.call_openrouter(prompt, max_tokens=500)
        
        if result:
            try:
                json_match = re.search(r'\{[\s\S]*\}', result)
                if json_match:
                    data = json.loads(json_match.group())
                    if "error" not in data and data.get("title"):
                        data["source"] = f"web:{urlparse(source_url).netloc}"
                        data["source_url"] = source_url
                        return data
            except json.JSONDecodeError:
                pass
        
        return None

    def _basic_web_scrape(self, url: str) -> List[Dict]:
        """Basic web scraping without Firecrawl"""
        from bs4 import BeautifulSoup
        
        events = []
        
        try:
            response = requests.get(url, timeout=30, headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
            })
            
            if response.status_code != 200:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract text content
            text = soup.get_text(separator="\n", strip=True)[:5000]
            
            # Use AI to find events
            prompt = f"""Find events mentioned on this webpage from {self.location}.

WEBPAGE CONTENT:
{text}

Return JSON array of events found:
[
    {{
        "title": "Event name",
        "date": "YYYY-MM-DD",
        "time": "HH:MM or null",
        "venue": "Venue name",
        "description": "Brief description",
        "category": "Category"
    }}
]

Return ONLY valid JSON array. If no events found, return []"""

            result = self.call_openrouter(prompt, max_tokens=2000)
            
            if result:
                try:
                    json_match = re.search(r'\[[\s\S]*\]', result)
                    if json_match:
                        events_data = json.loads(json_match.group())
                        for event in events_data:
                            event["source"] = f"web:{urlparse(url).netloc}"
                            event["source_url"] = url
                            events.append(event)
                except json.JSONDecodeError:
                    pass
            
        except Exception as e:
            self.log(f"Basic scrape error: {e}", "ERROR")
        
        return events

    def _is_url_scraped(self, url: str) -> bool:
        """Check if URL was already scraped"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM scraped_urls WHERE url = ?", (url,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

    def _mark_url_scraped(self, url: str, source: str):
        """Mark URL as scraped"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO scraped_urls (url, source) VALUES (?, ?)",
            (url, source)
        )
        conn.commit()
        conn.close()

    def save_event(self, event: Dict) -> bool:
        """Save event to database with deduplication"""
        title = event.get("title", "")
        date = event.get("date", "")
        venue = event.get("venue", "")
        
        if not title or not date:
            return False
        
        # Check for duplicates
        if self._is_duplicate(title, date, venue):
            self.log(f"Skipping duplicate: {title}", "INFO")
            return False
        
        unique_key = self._generate_unique_key(title, date, venue)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute("""
                INSERT INTO events (
                    unique_key, title, description, date, time, end_date,
                    venue, address, category, source, source_url, image_url,
                    price, is_free, is_featured
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                unique_key,
                title,
                event.get("description", ""),
                date,
                event.get("time"),
                event.get("end_date"),
                venue,
                event.get("address"),
                event.get("category", "Other"),
                event.get("source", ""),
                event.get("source_url", ""),
                event.get("image_url"),
                event.get("price"),
                event.get("is_free", False),
                event.get("is_featured", False)
            ))
            
            conn.commit()
            self.log(f"Saved event: {title}", "SUCCESS")
            return True
            
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def research_events(self) -> int:
        """Run full research - scrape all configured sources"""
        self.log("=" * 50, "INFO")
        self.log("Starting Event Research", "STEP")
        self.log("=" * 50, "INFO")
        
        total_events = 0
        
        # Scrape Instagram sources
        for handle in self.instagram_handles:
            events = self.scrape_instagram(handle)
            for event in events:
                if self.save_event(event):
                    total_events += 1
            time.sleep(1)  # Rate limiting between profiles
        
        # Scrape web sources
        for url in self.web_sources:
            events = self.scrape_web_source(url)
            for event in events:
                if self.save_event(event):
                    total_events += 1
            time.sleep(1)
        
        # Research local events via Perplexity with detailed descriptions
        if self.perplexity_key:
            self.log("Researching local events via Perplexity (detailed)", "STEP")
            query = f"""Find all events happening in {self.location} from {datetime.now().strftime('%B %d, %Y')} to {(datetime.now() + timedelta(days=self.days_ahead)).strftime('%B %d, %Y')}.

For EACH event, I need:
1. Event name
2. Exact date and time
3. Venue name and full address
4. Ticket price (or "Free" if free)
5. The official website URL or ticket purchase link where people can register or get more info
6. A compelling 2-3 sentence description that makes someone want to attend - describe the experience, atmosphere, and what makes it special

Include: concerts, live music shows, festivals, food & drink events, art exhibitions, markets, sports events, comedy shows, theater, family activities, and community gatherings.

IMPORTANT: Include the actual URL/link for each event where people can buy tickets or learn more."""
            
            perplexity_result = self.call_perplexity(query)
            if perplexity_result:
                # Parse and add events from Perplexity
                events = self._parse_perplexity_events(perplexity_result)
                for event in events:
                    if self.save_event(event):
                        total_events += 1
        
        self.log(f"Research complete. Total new events: {total_events}", "SUCCESS")
        return total_events

    def _parse_perplexity_events(self, text: str) -> List[Dict]:
        """Parse events from Perplexity research results"""
        prompt = f"""Extract ALL events from this research text. Create COMPELLING descriptions that make people want to attend.

LOCATION: {self.location}
CURRENT DATE: {datetime.now().strftime('%Y-%m-%d')}

TEXT:
{text[:4000]}

Return JSON array with COMPLETE event details:
[
    {{
        "title": "Event name",
        "date": "YYYY-MM-DD",
        "time": "7:00 PM" or null,
        "venue": "Venue name",
        "address": "Full address if available",
        "description": "Write an exciting 2-3 sentence description that SELLS the event - describe the vibe, what makes it unique, why someone shouldn't miss it. Make it sound appealing!",
        "price": "$25" or "Free" or "Varies",
        "is_free": true/false,
        "category": "Music & Nightlife" or "Food & Drink" or "Arts & Culture" or "Sports & Fitness" or "Family-Friendly" or "Other",
        "source_url": "The ticket/registration URL or official event page - MUST include if mentioned in text"
    }}
]

CRITICAL REQUIREMENTS:
- Write ENGAGING descriptions that advertise the event (not dry summaries)
- ALWAYS include source_url if any URL was mentioned for that event
- Extract ALL URLs mentioned (do512.com, eventbrite, venue websites, etc.)
- Only include events with specific dates within the next 7 days
- Return ONLY valid JSON array."""

        result = self.call_openrouter(prompt, max_tokens=3000)
        
        events = []
        if result:
            try:
                json_match = re.search(r'\[[\s\S]*\]', result)
                if json_match:
                    events_data = json.loads(json_match.group())
                    for event in events_data:
                        event["source"] = "perplexity:research"
                        # Ensure source_url is properly formatted
                        url = event.get("source_url")
                        if url and not url.startswith("http"):
                            event["source_url"] = f"https://{url}"
                        events.append(event)
            except json.JSONDecodeError:
                pass
        
        # Always enrich events with URLs if missing
        self._enrich_events_with_urls(events)
        
        return events
    
    def _enrich_events_with_urls(self, events: List[Dict]):
        """Add URLs to events that are missing them based on known sources"""
        # Common event/venue URL mappings (expandable per city)
        url_mappings = {
            # Austin Events
            "free week": "https://do512.com/p/free-week",
            "sxsw": "https://www.sxsw.com",
            "acl fest": "https://www.aclfestival.com",
            "austin city limits": "https://www.aclfestival.com",
            "fun fun fun fest": "https://funfunfunfest.com",
            "austin fc": "https://www.austinfc.com/tickets",
            "gem show": "https://intergem.com",
            "jewelry show": "https://intergem.com",
            "vintage sale": "https://www.citywidevintagesale.com",
            "city-wide vintage": "https://www.citywidevintagesale.com",
            "rodeo austin": "https://www.rodeoaustin.com",
            "trail of lights": "https://austintrailoflights.org",
            "pecan street festival": "https://pecanstreetfestival.org",
            "hot sauce festival": "https://austinchronicle.com/hot-sauce-festival",
            "blues on the green": "https://www.acl-live.com/blues-on-the-green",
            # Austin Venues
            "stubb's": "https://stubbsaustin.com",
            "stubbs": "https://stubbsaustin.com",
            "mohawk": "https://mohawkaustin.com",
            "emo's": "https://emosaustin.com",
            "emos": "https://emosaustin.com",
            "paramount": "https://www.austintheatre.org",
            "paramount theatre": "https://www.austintheatre.org",
            "state theatre": "https://www.austintheatre.org",
            "zach theatre": "https://zachtheatre.org",
            "zach theater": "https://zachtheatre.org",
            "long center": "https://thelongcenter.org",
            "acl live": "https://www.acl-live.com",
            "moody theater": "https://www.acl-live.com",
            "moody center": "https://moodycenteratx.com",
            "q2 stadium": "https://www.austinfc.com",
            "circuit of the americas": "https://www.circuitoftheamericas.com",
            "cota": "https://www.circuitoftheamericas.com",
            "blanton museum": "https://blantonmuseum.org",
            "bob bullock museum": "https://www.thestoryoftexas.com",
            "hope outdoor gallery": "https://www.hopeoutdoorgallery.com",
            "empire control room": "https://www.empireatx.com",
            "vulcan gas company": "https://www.vulcanatx.com",
            "antone's": "https://antonesnightclub.com",
            "antones": "https://antonesnightclub.com",
            "continental club": "https://continentalclub.com",
            "broken spoke": "https://www.brokenspokeaustintx.net",
            "saxon pub": "https://thesaxonpub.com",
            "parish": "https://www.parishatx.com",
            "scoot inn": "https://scootinnaustin.com",
            "hole in the wall": "https://www.holeinthewallaustin.com",
            "cap city comedy": "https://capcitycomedy.com",
            "creek and the cave": "https://creekandcave.com",
            "alamo drafthouse": "https://drafthouse.com/austin",
            "barton springs": "https://www.austintexas.gov/department/barton-springs-pool",
            "zilker park": "https://www.austintexas.gov/department/zilker-metropolitan-park",
            "mueller": "https://www.muelleraustin.com",
            "domain": "https://www.domainnorthside.com",
            "farmers market": "https://texasfarmersmarket.org",
        }
        
        # Detect city from location for fallback search
        city = self.location.split(",")[0].strip().lower() if self.location else "austin"
        
        # City-specific search URLs
        search_urls = {
            "austin": "https://do512.com/events?q=",
            "dallas": "https://www.dallas.com/events/?search=",
            "houston": "https://www.houston.org/events?search=",
            "san antonio": "https://www.visitsanantonio.com/events/?search=",
            "default": "https://www.eventbrite.com/d/united-states/events/?q="
        }
        
        base_search_url = search_urls.get(city, search_urls["default"])
        
        for event in events:
            if not event.get("source_url"):
                title_lower = event.get("title", "").lower()
                venue_lower = event.get("venue", "").lower()
                
                # Check title and venue against mappings
                for keyword, url in url_mappings.items():
                    if keyword in title_lower or keyword in venue_lower:
                        event["source_url"] = url
                        break
                
                # Fallback to search URL if no match
                if not event.get("source_url"):
                    search_term = event.get("title", "").replace(" ", "+")
                    event["source_url"] = f"{base_search_url}{search_term}"

    def get_upcoming_events(self) -> Dict[str, List[Dict]]:
        """Get upcoming events grouped by category"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        start_date = datetime.now().strftime("%Y-%m-%d")
        end_date = (datetime.now() + timedelta(days=self.days_ahead)).strftime("%Y-%m-%d")
        
        cursor.execute("""
            SELECT * FROM events 
            WHERE date BETWEEN ? AND ?
            ORDER BY is_featured DESC, date ASC, time ASC
        """, (start_date, end_date))
        
        rows = cursor.fetchall()
        conn.close()
        
        # Group by category
        events_by_category = {cat: [] for cat in self.DEFAULT_CATEGORIES}
        
        for row in rows:
            event = dict(row)
            category = event.get("category", "Other")
            if category not in events_by_category:
                category = "Other"
            events_by_category[category].append(event)
        
        # Move featured events to their own section
        featured = []
        for category, events in events_by_category.items():
            for event in events[:]:
                if event.get("is_featured"):
                    featured.append(event)
                    events.remove(event)
        
        events_by_category["Featured Events"] = featured[:5]  # Top 5 featured
        
        # Also collect free events
        free_events = []
        for category, events in events_by_category.items():
            if category != "Free Events":
                for event in events:
                    if event.get("is_free"):
                        free_events.append(event)
        events_by_category["Free Events"] = free_events[:10]
        
        return events_by_category

    def generate_newsletter(self) -> str:
        """Generate the newsletter content"""
        self.log("=" * 50, "INFO")
        self.log("Generating Newsletter", "STEP")
        self.log("=" * 50, "INFO")
        
        events_by_category = self.get_upcoming_events()
        
        total_events = sum(len(events) for events in events_by_category.values())
        if total_events == 0:
            self.log("No events found for newsletter", "WARNING")
            return ""
        
        self.log(f"Found {total_events} events across {len(events_by_category)} categories", "INFO")
        
        # Generate date range string
        start_date = datetime.now()
        end_date = start_date + timedelta(days=self.days_ahead)
        date_range = f"{start_date.strftime('%B %d')} - {end_date.strftime('%B %d, %Y')}"
        
        # Generate AI intro
        top_events = []
        for events in events_by_category.values():
            top_events.extend(events[:2])
        
        intro_prompt = f"""Write a 2-3 sentence intro for a local events newsletter for {self.location}.

TOP EVENTS THIS WEEK:
{json.dumps([e.get('title') for e in top_events[:5]], indent=2)}

Make it friendly, exciting, and make readers want to explore the events.
Keep it under 50 words. Don't use generic phrases like "exciting week ahead"."""

        intro = self.call_openrouter(intro_prompt, max_tokens=150) or \
            f"Here's what's happening in {self.location} this week!"
        
        # Build newsletter
        newsletter = f"""# {self.newsletter_name} 📰
**Week of {date_range} | {self.location}**

---

## 👋 Hey {self.location.split(',')[0]} locals!

{intro}

---

"""
        
        # Add each category section
        for category in self.DEFAULT_CATEGORIES:
            events = events_by_category.get(category, [])
            if not events:
                continue
            
            emoji = {
                "Featured Events": "⭐",
                "Music & Nightlife": "🎵",
                "Food & Drink": "🍔",
                "Arts & Culture": "🎨",
                "Sports & Fitness": "🏃",
                "Family-Friendly": "👨‍👩‍👧‍👦",
                "Free Events": "💸",
                "Other": "📌"
            }.get(category, "📌")
            
            newsletter += f"## {emoji} {category}\n\n"
            
            if category == "Featured Events":
                # Full details for featured
                for event in events[:5]:
                    newsletter += self._format_featured_event(event)
            else:
                # Table format for others
                newsletter += "| Event | When | Where | Price |\n"
                newsletter += "|-------|------|-------|-------|\n"
                for event in events[:10]:
                    newsletter += self._format_table_event(event)
            
            newsletter += "\n---\n\n"
        
        # Add footer
        newsletter += f"""## 📍 Quick Links

Want to explore more? Check out our source calendars.

---

**Enjoying {self.newsletter_name}?** Forward this to a friend who needs to know what's happening in {self.location}!

[Unsubscribe](#) | [Preferences](#) | [Forward to a Friend](#)

---

*Generated with AI assistance. Event details may change - always confirm with the venue.*
"""
        
        # Save newsletter
        timestamp = datetime.now().strftime("%Y-%m-%d")
        output_path = self.base_dir / f"newsletter_{timestamp}.md"
        output_path.write_text(newsletter, encoding="utf-8")
        
        # Also save HTML version
        html_path = self.base_dir / f"newsletter_{timestamp}.html"
        html_content = self._convert_to_html(newsletter)
        html_path.write_text(html_content, encoding="utf-8")
        
        # Generate email-optimized HTML for ConvertKit
        email_html = self._generate_beehiiv_html(events_by_category, intro, date_range)
        email_path = self.base_dir / f"newsletter_{timestamp}_email.html"
        email_path.write_text(email_html, encoding="utf-8")
        
        self.log(f"Newsletter saved: {output_path}", "SUCCESS")
        self.log(f"HTML version saved: {html_path}", "SUCCESS")
        self.log(f"Email HTML saved: {email_path}", "SUCCESS")
        
        # Publish to ConvertKit if enabled
        if self.publish_to_convertkit:
            subject = f"{self.newsletter_name} - Week of {start_date.strftime('%B %d')}"
            preview = f"What's happening in {self.location} this week"
            self.publish_to_convertkit_api(email_html, subject, preview)
        
        return newsletter

    def _format_featured_event(self, event: Dict) -> str:
        """Format a featured event with full details"""
        title = event.get("title", "Untitled")
        date = event.get("date", "TBD")
        time = event.get("time", "")
        venue = event.get("venue", "TBD")
        description = event.get("description", "")
        price = event.get("price", "")
        source_url = event.get("source_url", "")
        
        # Format date nicely
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_str = date_obj.strftime("%A, %B %d")
        except:
            date_str = date
        
        time_str = f" at {time}" if time else ""
        price_str = f"**Price:** {price}" if price else ""
        link_str = f"[More info]({source_url})" if source_url else ""
        
        return f"""### {title}

📅 {date_str}{time_str}
📍 {venue}
{price_str}

{description}

{link_str}

---

"""

    def _format_table_event(self, event: Dict) -> str:
        """Format event as table row"""
        title = event.get("title", "Untitled")[:40]
        date = event.get("date", "TBD")
        time = event.get("time", "")
        venue = event.get("venue", "TBD")[:25]
        price = event.get("price", "-")
        source_url = event.get("source_url", "")
        
        # Format date
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_str = date_obj.strftime("%a %m/%d")
        except:
            date_str = date
        
        when = f"{date_str} {time}".strip()
        
        if source_url:
            title = f"[{title}]({source_url})"
        
        return f"| {title} | {when} | {venue} | {price} |\n"

    def _convert_to_html(self, markdown: str) -> str:
        """Convert markdown to basic HTML for email"""
        try:
            import markdown as md
            html_body = md.markdown(markdown, extensions=['tables'])
        except ImportError:
            # Basic conversion without markdown library
            html_body = markdown.replace("\n", "<br>")
        
        html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.newsletter_name}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{ color: #1a1a1a; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #2c2c2c; margin-top: 30px; }}
        h3 {{ color: #444; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #f5f5f5; }}
        a {{ color: #0066cc; }}
        hr {{ border: none; border-top: 1px solid #eee; margin: 20px 0; }}
    </style>
</head>
<body>
{html_body}
</body>
</html>"""
        
        return html

    def _generate_beehiiv_html(self, events_by_category: Dict, intro: str, date_range: str) -> str:
        """Generate beautifully formatted HTML email for ConvertKit"""
        
        # Color scheme
        primary_color = "#6366f1"  # Indigo
        secondary_color = "#8b5cf6"  # Purple  
        accent_color = "#f59e0b"  # Amber
        text_dark = "#1f2937"
        text_muted = "#6b7280"
        bg_light = "#f9fafb"
        border_color = "#e5e7eb"
        
        # Build event sections
        event_sections = ""
        
        category_styles = {
            "Featured Events": {"emoji": "⭐", "color": "#f59e0b", "bg": "#fef3c7"},
            "Music & Nightlife": {"emoji": "🎵", "color": "#8b5cf6", "bg": "#ede9fe"},
            "Food & Drink": {"emoji": "🍔", "color": "#ef4444", "bg": "#fee2e2"},
            "Arts & Culture": {"emoji": "🎨", "color": "#ec4899", "bg": "#fce7f3"},
            "Sports & Fitness": {"emoji": "🏃", "color": "#10b981", "bg": "#d1fae5"},
            "Family-Friendly": {"emoji": "👨‍👩‍👧‍👦", "color": "#3b82f6", "bg": "#dbeafe"},
            "Free Events": {"emoji": "💸", "color": "#22c55e", "bg": "#dcfce7"},
            "Other": {"emoji": "📌", "color": "#6366f1", "bg": "#e0e7ff"}
        }
        
        for category in self.DEFAULT_CATEGORIES:
            events = events_by_category.get(category, [])
            if not events:
                continue
            
            style = category_styles.get(category, category_styles["Other"])
            
            event_sections += f'''
            <!-- {category} Section -->
            <tr>
                <td style="padding: 0 0 30px 0;">
                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                        <tr>
                            <td style="padding: 12px 16px; background: {style['bg']}; border-radius: 8px 8px 0 0; border-left: 4px solid {style['color']};">
                                <span style="font-size: 20px; font-weight: 700; color: {text_dark};">{style['emoji']} {category}</span>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 0; background: #ffffff; border: 1px solid {border_color}; border-top: none; border-radius: 0 0 8px 8px;">
'''
            
            if category == "Featured Events":
                for event in events[:3]:
                    event_sections += self._format_featured_event_html(event, style['color'])
            else:
                for event in events[:6]:
                    event_sections += self._format_event_card_html(event)
            
            event_sections += '''
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>
'''
        
        # Get header image from Unsplash
        header_image = self.get_header_image()
        
        # Build header style based on whether we have an image
        if header_image:
            header_style = f'''background: linear-gradient(rgba(30, 30, 30, 0.6), rgba(30, 30, 30, 0.6)), url('{header_image}'); background-size: cover; background-position: center;'''
        else:
            header_style = f'''background: linear-gradient(135deg, {primary_color} 0%, {secondary_color} 100%);'''
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.newsletter_name}</title>
    <!--[if mso]>
    <style type="text/css">
        body, table, td {{font-family: Arial, Helvetica, sans-serif !important;}}
    </style>
    <![endif]-->
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
</head>
<body style="margin: 0; padding: 0; background-color: #f3f4f6; font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
    
    <!-- Email Container -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color: #f3f4f6;">
        <tr>
            <td align="center" style="padding: 40px 20px;">
                
                <!-- Content Container -->
                <table width="600" cellpadding="0" cellspacing="0" border="0" style="max-width: 600px; width: 100%;">
                    
                    <!-- Header with Image -->
                    <tr>
                        <td style="{header_style} padding: 50px 30px; border-radius: 16px 16px 0 0; text-align: center;">
                            <h1 style="margin: 0 0 12px 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 38px; font-weight: 800; color: #ffffff; letter-spacing: -1px; text-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                                {self.newsletter_name}
                            </h1>
                            <p style="margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 16px; font-weight: 500; color: rgba(255,255,255,0.95); text-shadow: 0 1px 2px rgba(0,0,0,0.2);">
                                {date_range} • {self.location}
                            </p>
                        </td>
                    </tr>
                    
                    <!-- Main Content -->
                    <tr>
                        <td style="background: #ffffff; padding: 30px;">
                            
                            <!-- Intro Section -->
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td style="padding: 0 0 30px 0;">
                                        <p style="margin: 0 0 16px 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 26px; font-weight: 700; color: {text_dark};">
                                            Hey {self.location.split(',')[0]} locals! 👋
                                        </p>
                                        <p style="margin: 0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 16px; line-height: 1.7; color: {text_muted};">
                                            {intro}
                                        </p>
                                    </td>
                                </tr>
                                
                                <!-- Divider -->
                                <tr>
                                    <td style="padding: 0 0 30px 0;">
                                        <div style="height: 2px; background: linear-gradient(90deg, {primary_color}, {secondary_color}, {accent_color}); border-radius: 2px;"></div>
                                    </td>
                                </tr>
                                
                                {event_sections}
                                
                            </table>
                            
                        </td>
                    </tr>
                    
                    <!-- Footer -->
                    <tr>
                        <td style="background: {bg_light}; padding: 30px; border-radius: 0 0 16px 16px; border-top: 1px solid {border_color};">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td style="text-align: center; padding-bottom: 20px;">
                                        <p style="margin: 0 0 8px 0; font-size: 18px; font-weight: 700; color: {text_dark};">
                                            Enjoying {self.newsletter_name}?
                                        </p>
                                        <p style="margin: 0; font-size: 14px; color: {text_muted};">
                                            Forward this to a friend who wants to know what's happening in {self.location}!
                                        </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td style="text-align: center;">
                                        <p style="margin: 0; font-size: 12px; color: #9ca3af;">
                                            Event details may change — always confirm with the venue.<br>
                                            <a href="#" style="color: {primary_color}; text-decoration: none;">Unsubscribe</a> • 
                                            <a href="#" style="color: {primary_color}; text-decoration: none;">Preferences</a>
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                </table>
                
            </td>
        </tr>
    </table>
    
</body>
</html>'''
        
        return html

    def _format_featured_event_html(self, event: Dict, accent_color: str = "#f59e0b") -> str:
        """Format a featured event as a beautiful HTML card"""
        title = event.get("title", "Untitled")
        date = event.get("date", "TBD")
        time = event.get("time", "")
        venue = event.get("venue", "TBD")
        description = event.get("description", "")
        price = event.get("price", "")
        source_url = event.get("source_url", "")
        
        # Format date
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_str = date_obj.strftime("%A, %B %d")
        except:
            date_str = date
        
        time_str = f" at {time}" if time else ""
        
        # Build link
        title_html = f'<a href="{source_url}" style="color: #1f2937; text-decoration: none;">{title}</a>' if source_url else title
        
        html = f'''
                                <div style="padding: 20px; border-bottom: 1px solid #e5e7eb;">
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                        <tr>
                                            <td>
                                                <h3 style="margin: 0 0 12px 0; font-size: 18px; font-weight: 700; color: #1f2937;">
                                                    {title_html}
                                                </h3>
                                                <table cellpadding="0" cellspacing="0" border="0">
                                                    <tr>
                                                        <td style="padding-right: 20px;">
                                                            <span style="font-size: 14px; color: #6b7280;">
                                                                📅 <strong style="color: #374151;">{date_str}{time_str}</strong>
                                                            </span>
                                                        </td>
                                                        <td>
                                                            <span style="font-size: 14px; color: #6b7280;">
                                                                📍 {venue}
                                                            </span>
                                                        </td>
                                                    </tr>
                                                </table>
'''
        
        if description:
            html += f'''
                                                <p style="margin: 12px 0 0 0; font-size: 14px; line-height: 1.5; color: #6b7280;">
                                                    {description[:150]}{'...' if len(description) > 150 else ''}
                                                </p>
'''
        
        if price:
            html += f'''
                                                <p style="margin: 12px 0 0 0;">
                                                    <span style="display: inline-block; padding: 4px 10px; background: #dcfce7; color: #166534; font-size: 12px; font-weight: 600; border-radius: 12px;">
                                                        {price}
                                                    </span>
                                                </p>
'''
        
        if source_url:
            html += f'''
                                                <p style="margin: 16px 0 0 0;">
                                                    <a href="{source_url}" style="display: inline-block; padding: 8px 16px; background: {accent_color}; color: #ffffff; font-size: 13px; font-weight: 600; text-decoration: none; border-radius: 6px;">
                                                        Learn More →
                                                    </a>
                                                </p>
'''
        
        html += '''
                                            </td>
                                        </tr>
                                    </table>
                                </div>
'''
        return html

    def _format_event_card_html(self, event: Dict) -> str:
        """Format an event as a card with description"""
        title = event.get("title", "Untitled")
        date = event.get("date", "TBD")
        time = event.get("time", "")
        venue = event.get("venue", "TBD")
        description = event.get("description", "")
        source_url = event.get("source_url", "")
        price = event.get("price", "")
        
        # Format date
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            date_str = date_obj.strftime("%a, %b %d")
        except:
            date_str = date
        
        time_str = f" • {time}" if time else ""
        
        # Build link
        title_html = f'<a href="{source_url}" style="color: #1f2937; text-decoration: none; font-weight: 700;">{title}</a>' if source_url else f'<span style="font-weight: 700; color: #1f2937;">{title}</span>'
        
        html = f'''
                                <div style="padding: 20px; border-bottom: 1px solid #e5e7eb;">
                                    <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                        <tr>
                                            <td style="vertical-align: top;">
                                                <p style="margin: 0 0 8px 0; font-size: 17px; font-family: 'Inter', -apple-system, sans-serif;">
                                                    {title_html}
                                                </p>
                                                <p style="margin: 0 0 10px 0; font-size: 13px; color: #6b7280;">
                                                    📅 {date_str}{time_str} &nbsp;•&nbsp; 📍 {venue}
                                                </p>
'''
        
        if description:
            html += f'''
                                                <p style="margin: 0 0 12px 0; font-size: 14px; line-height: 1.6; color: #4b5563; font-family: 'Inter', -apple-system, sans-serif;">
                                                    {description}
                                                </p>
'''
        
        # Add price badge and link button
        html += f'''
                                                <table cellpadding="0" cellspacing="0" border="0">
                                                    <tr>
'''
        if price:
            html += f'''
                                                        <td style="padding-right: 12px;">
                                                            <span style="display: inline-block; padding: 4px 10px; background: #f3f4f6; color: #374151; font-size: 12px; font-weight: 600; border-radius: 4px;">
                                                                {price}
                                                            </span>
                                                        </td>
'''
        if source_url:
            html += f'''
                                                        <td>
                                                            <a href="{source_url}" style="display: inline-block; padding: 6px 14px; background: #6366f1; color: #ffffff; font-size: 12px; font-weight: 600; text-decoration: none; border-radius: 4px;">
                                                                Get Tickets →
                                                            </a>
                                                        </td>
'''
        html += '''
                                                    </tr>
                                                </table>
                                            </td>
                                        </tr>
                                    </table>
                                </div>
'''
        return html

    def publish_to_convertkit_api(self, html_content: str, subject: str, preview_text: str = "") -> Optional[Dict]:
        """Publish newsletter to ConvertKit/Kit via API v4"""
        if not self.convertkit_key:
            self.log("CONVERTKIT_API_KEY not set", "ERROR")
            return None
        
        self.log(f"Publishing to ConvertKit ({self.publish_status})...", "STEP")
        
        url = "https://api.kit.com/v4/broadcasts"
        
        headers = {
            "X-Kit-Api-Key": self.convertkit_key,
            "Content-Type": "application/json"
        }
        
        # Build the payload
        payload = {
            "subject": subject,
            "content": html_content,
            "description": preview_text or subject,  # Preview text in inbox
            "public": True,  # Make it viewable on web
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=60)
            
            if response.status_code in [200, 201]:
                data = response.json()
                broadcast = data.get("broadcast", {})
                broadcast_id = broadcast.get("id", "")
                self.log(f"Created ConvertKit broadcast! ID: {broadcast_id}", "SUCCESS")
                
                # If status is "send", send the broadcast now
                if self.publish_status == "send":
                    return self._send_convertkit_broadcast(broadcast_id)
                else:
                    self.log(f"Broadcast saved as draft. Go to Kit dashboard to send.", "INFO")
                
                return data
            else:
                self.log(f"ConvertKit API error: {response.status_code} - {response.text[:500]}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"ConvertKit publish error: {e}", "ERROR")
            return None

    def _send_convertkit_broadcast(self, broadcast_id: str) -> Optional[Dict]:
        """Send a ConvertKit broadcast immediately"""
        self.log(f"Sending broadcast {broadcast_id}...", "STEP")
        
        url = f"https://api.kit.com/v4/broadcasts/{broadcast_id}/send"
        
        headers = {
            "X-Kit-Api-Key": self.convertkit_key,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, headers=headers, timeout=60)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.log(f"Broadcast sent successfully!", "SUCCESS")
                return data
            else:
                self.log(f"ConvertKit send error: {response.status_code} - {response.text[:500]}", "ERROR")
                return None
                
        except Exception as e:
            self.log(f"ConvertKit send error: {e}", "ERROR")
            return None

    def setup_config(self):
        """Interactive setup for newsletter configuration"""
        self.log("Setting up newsletter configuration", "STEP")
        
        config = {
            "location": self.location,
            "newsletter_name": self.newsletter_name,
            "frequency": "weekly",
            "days_ahead": self.days_ahead,
            "instagram": [
                {"handle": h, "category": "events", "priority": "medium"}
                for h in self.instagram_handles
            ] if self.instagram_handles else [],
            "web_aggregators": [
                {"url": u, "name": urlparse(u).netloc, "discovery_method": "crawl"}
                for u in self.web_sources
            ] if self.web_sources else [],
            "sections": self.DEFAULT_CATEGORIES,
            "created_at": datetime.now().isoformat()
        }
        
        if YAML_AVAILABLE:
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
        else:
            # Save as JSON fallback
            config_path = self.config_path.with_suffix('.json')
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
        
        self.log(f"Configuration saved: {self.config_path}", "SUCCESS")
        
        return config

    def full_run(self) -> Dict:
        """Execute full newsletter generation pipeline"""
        self.log("=" * 60, "INFO")
        self.log(f"🚀 FULL NEWSLETTER RUN: {self.newsletter_name}", "INFO")
        self.log(f"   Location: {self.location}", "INFO")
        self.log(f"   Looking ahead: {self.days_ahead} days", "INFO")
        self.log("=" * 60, "INFO")
        
        start_time = time.time()
        
        # Step 1: Research events
        events_found = self.research_events()
        
        # Step 2: Generate newsletter
        newsletter = self.generate_newsletter()
        
        execution_time = time.time() - start_time
        
        result = {
            "success": bool(newsletter),
            "location": self.location,
            "newsletter_name": self.newsletter_name,
            "events_found": events_found,
            "execution_time": f"{int(execution_time)}s",
            "output_dir": str(self.base_dir),
            "newsletter_path": str(self.base_dir / f"newsletter_{datetime.now().strftime('%Y-%m-%d')}.md")
        }
        
        # Save result
        result_path = self.base_dir / "last_run.json"
        with open(result_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.log("=" * 60, "INFO")
        self.log(f"✅ NEWSLETTER GENERATION COMPLETE", "SUCCESS")
        self.log(f"   Events found: {events_found}", "INFO")
        self.log(f"   Output: {self.base_dir}", "INFO")
        self.log(f"   Time: {int(execution_time)}s", "INFO")
        self.log("=" * 60, "INFO")
        
        return result


def main():
    parser = argparse.ArgumentParser(
        description="Generate local newsletters automatically",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Full automation
  python3 execution/generate_local_newsletter.py \\
      --location "Austin, TX" \\
      --instagram "@do512,@austin_events" \\
      --newsletter-name "Austin Weekly"
  
  # Setup only
  python3 execution/generate_local_newsletter.py --setup --location "Austin, TX"
  
  # Research only
  python3 execution/generate_local_newsletter.py --research --location "Austin, TX"
  
  # Write only (uses existing data)
  python3 execution/generate_local_newsletter.py --write --location "Austin, TX"
        """
    )
    
    # Action arguments
    parser.add_argument("--setup", action="store_true", help="Setup configuration")
    parser.add_argument("--research", action="store_true", help="Research and scrape events")
    parser.add_argument("--write", action="store_true", help="Generate newsletter from existing data")
    parser.add_argument("--full-run", action="store_true", help="Run complete pipeline")
    
    # Configuration
    parser.add_argument("--location", required=True, help="Location (e.g., 'Austin, TX')")
    parser.add_argument("--newsletter-name", help="Name of newsletter")
    parser.add_argument("--days", type=int, default=7, help="Days ahead to look (default: 7)")
    
    # Sources
    parser.add_argument("--instagram", help="Comma-separated Instagram handles")
    parser.add_argument("--web-sources", help="Comma-separated web URLs")
    parser.add_argument("--facebook-urls", help="Comma-separated Facebook event URLs")
    
    # Template
    parser.add_argument("--template", default="weekly", 
                       choices=["weekly", "weekend", "daily", "monthly"])
    
    # Publishing
    parser.add_argument("--publish", action="store_true", 
                       help="Publish directly to ConvertKit/Kit")
    parser.add_argument("--publish-status", default="draft",
                       choices=["draft", "send"],
                       help="ConvertKit status (draft=save only, send=publish immediately)")
    
    args = parser.parse_args()
    
    # Parse list arguments
    instagram = [h.strip() for h in args.instagram.split(",")] if args.instagram else []
    web_sources = [u.strip() for u in args.web_sources.split(",")] if args.web_sources else []
    facebook_urls = [u.strip() for u in args.facebook_urls.split(",")] if args.facebook_urls else []
    
    # Create generator
    generator = LocalNewsletterGenerator(
        location=args.location,
        newsletter_name=args.newsletter_name or f"{args.location.split(',')[0]} Weekly",
        days=args.days,
        instagram=instagram,
        web_sources=web_sources,
        facebook_urls=facebook_urls,
        template=args.template,
        publish=args.publish,
        publish_status=args.publish_status
    )
    
    # Execute requested action
    if args.setup:
        generator.setup_config()
    elif args.research:
        generator.research_events()
    elif args.write:
        generator.generate_newsletter()
    elif args.full_run:
        result = generator.full_run()
        return 0 if result["success"] else 1
    else:
        # Default to full run
        result = generator.full_run()
        return 0 if result["success"] else 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
