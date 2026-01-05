#!/usr/bin/env python3
"""
Upwork job scraper using Playwright to bypass Cloudflare.
"""

import json
import time
import re
from playwright.sync_api import sync_playwright


def scrape_upwork_jobs(query: str, max_pages: int = 1) -> list[dict]:
    """Scrape Upwork jobs for a given search query."""

    jobs = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        for page_num in range(1, max_pages + 1):
            url = f"https://www.upwork.com/nx/search/jobs/?q={query}&page={page_num}"
            print(f"Fetching page {page_num}: {url}")

            page.goto(url, wait_until="networkidle", timeout=60000)
            time.sleep(3)  # Let JS render

            # Check for Cloudflare challenge
            if "challenge" in page.url or "cf-" in page.content()[:1000].lower():
                print("Cloudflare challenge detected, waiting...")
                time.sleep(5)
                page.reload(wait_until="networkidle")
                time.sleep(3)

            # Find all job tiles
            job_tiles = page.query_selector_all('[data-test="JobTile"]')
            print(f"Found {len(job_tiles)} jobs on page {page_num}")

            for tile in job_tiles:
                try:
                    job = extract_job_data(tile)
                    if job:
                        jobs.append(job)
                except Exception as e:
                    print(f"Error extracting job: {e}")
                    continue

        browser.close()

    return jobs


def extract_job_data(tile) -> dict:
    """Extract job data from a job tile element."""

    job = {}

    # Job ID
    job_uid = tile.get_attribute("data-ev-job-uid")
    job['id'] = job_uid

    # Title and URL
    title_link = tile.query_selector('[data-test="job-tile-title-link"]')
    if title_link:
        job['title'] = clean_text(title_link.inner_text())
        href = title_link.get_attribute("href")
        job['url'] = f"https://www.upwork.com{href}" if href else None

    # Posted date
    posted = tile.query_selector('[data-test="job-pubilshed-date"]')
    if posted:
        job['posted'] = clean_text(posted.inner_text())

    # Description
    desc = tile.query_selector('[data-test="JobDescription"]')
    if desc:
        job['description'] = clean_text(desc.inner_text())

    # Job info (type, level, budget/rate, duration)
    job_info = tile.query_selector('[data-test="JobInfo"]')
    if job_info:
        info_items = job_info.query_selector_all("li")
        for item in info_items:
            text = clean_text(item.inner_text())
            test_attr = item.get_attribute("data-test")

            if test_attr == "job-type-label":
                job['job_type'] = text
            elif test_attr == "experience-level":
                job['experience_level'] = text
            elif test_attr == "is-fixed-price":
                job['budget'] = text
            elif test_attr == "duration-label":
                job['duration'] = text

    # Client info
    client_info = tile.query_selector('[data-test="JobInfoClient"]')
    if client_info:
        # Payment verified
        payment = client_info.query_selector('[data-test="payment-verified"]')
        if payment:
            job['payment_verified'] = "verified" in payment.inner_text().lower()

        # Rating
        rating = client_info.query_selector('[data-test="feedback-rating"]')
        if rating:
            rating_text = rating.query_selector('.air3-rating-value-text')
            if rating_text:
                job['client_rating'] = clean_text(rating_text.inner_text())

        # Total spent
        spent = client_info.query_selector('[data-test="total-spent"]')
        if spent:
            job['client_spent'] = clean_text(spent.inner_text())

        # Location
        location = client_info.query_selector('[data-test="location"]')
        if location:
            job['client_location'] = clean_text(location.inner_text())

    # Skills/tags
    skills_container = tile.query_selector('[data-test="TokenClamp JobAttrs"]')
    if skills_container:
        skill_buttons = skills_container.query_selector_all('[data-test="token"]')
        job['skills'] = [clean_text(btn.inner_text()) for btn in skill_buttons]

    # Proposals
    proposals = tile.query_selector('[data-test="proposals-tier"]')
    if proposals:
        job['proposals'] = clean_text(proposals.inner_text())

    return job


def clean_text(text: str) -> str:
    """Clean extracted text."""
    if not text:
        return ""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Scrape Upwork jobs")
    parser.add_argument("--query", "-q", default="automation", help="Search query")
    parser.add_argument("--pages", "-p", type=int, default=1, help="Number of pages")
    parser.add_argument("--output", "-o", help="Output JSON file")

    args = parser.parse_args()

    print(f"Scraping Upwork for: {args.query}")
    jobs = scrape_upwork_jobs(args.query, args.pages)

    print(f"\n=== Found {len(jobs)} jobs ===\n")

    for i, job in enumerate(jobs[:5], 1):  # Show first 5
        print(f"{i}. {job.get('title', 'N/A')}")
        print(f"   {job.get('job_type', '')} | {job.get('experience_level', '')} | {job.get('budget', job.get('duration', ''))}")
        print(f"   Client: {job.get('client_location', 'N/A')} | {job.get('client_spent', 'N/A')} | Rating: {job.get('client_rating', 'N/A')}")
        print(f"   Skills: {', '.join(job.get('skills', []))}")
        print()

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(jobs, f, indent=2)
        print(f"Saved {len(jobs)} jobs to {args.output}")

    return jobs


if __name__ == "__main__":
    main()
