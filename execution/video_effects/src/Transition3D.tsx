import React from "react";
import {
  AbsoluteFill,
  Img,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  spring,
  Easing,
} from "remotion";

interface Transition3DProps {
  // Image sequence or video frames
  imageSrc: string;
  // Start rotation values (in degrees)
  startSwivel?: number; // Y-axis rotation
  startTilt?: number; // X-axis rotation
  // End rotation values
  endSwivel?: number;
  endTilt?: number;
  // Perspective depth
  perspective?: number;
  // Easing type
  easeType?: "spring" | "easeOut" | "easeInOut";
}

export const Transition3D: React.FC<Transition3DProps> = ({
  imageSrc,
  startSwivel = -30,
  startTilt = 15,
  endSwivel = 0,
  endTilt = 0,
  perspective = 1000,
  easeType = "easeOut",
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // Calculate progress (0 to 1)
  let progress: number;

  if (easeType === "spring") {
    progress = spring({
      frame,
      fps,
      config: {
        damping: 20,
        stiffness: 100,
        mass: 0.5,
      },
    });
  } else if (easeType === "easeOut") {
    progress = interpolate(frame, [0, durationInFrames], [0, 1], {
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });
  } else {
    progress = interpolate(frame, [0, durationInFrames], [0, 1], {
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.cubic),
    });
  }

  // Interpolate rotation values
  const swivel = interpolate(progress, [0, 1], [startSwivel, endSwivel]);
  const tilt = interpolate(progress, [0, 1], [startTilt, endTilt]);

  // Optional: Add slight zoom effect for more drama
  const scale = interpolate(progress, [0, 1], [1.1, 1]);

  return (
    <AbsoluteFill
      style={{
        perspective: `${perspective}px`,
        backgroundColor: "black",
      }}
    >
      <AbsoluteFill
        style={{
          transform: `rotateY(${swivel}deg) rotateX(${tilt}deg) scale(${scale})`,
          transformStyle: "preserve-3d",
          backfaceVisibility: "hidden",
        }}
      >
        <Img
          src={imageSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Version that works with video (using OffthreadVideo)
export const Transition3DVideo: React.FC<{
  videoSrc: string;
  startSwivel?: number;
  startTilt?: number;
  endSwivel?: number;
  endTilt?: number;
  perspective?: number;
  easeType?: "spring" | "easeOut" | "easeInOut";
  playbackRate?: number;
}> = ({
  videoSrc,
  startSwivel = -30,
  startTilt = 15,
  endSwivel = 0,
  endTilt = 0,
  perspective = 1000,
  easeType = "easeOut",
  playbackRate = 7, // 700% speed like the editor's example
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  let progress: number;

  if (easeType === "spring") {
    progress = spring({
      frame,
      fps,
      config: {
        damping: 20,
        stiffness: 100,
        mass: 0.5,
      },
    });
  } else if (easeType === "easeOut") {
    progress = interpolate(frame, [0, durationInFrames], [0, 1], {
      extrapolateRight: "clamp",
      easing: Easing.out(Easing.cubic),
    });
  } else {
    progress = interpolate(frame, [0, durationInFrames], [0, 1], {
      extrapolateRight: "clamp",
      easing: Easing.inOut(Easing.cubic),
    });
  }

  const swivel = interpolate(progress, [0, 1], [startSwivel, endSwivel]);
  const tilt = interpolate(progress, [0, 1], [startTilt, endTilt]);
  const scale = interpolate(progress, [0, 1], [1.1, 1]);

  // We need to use OffthreadVideo for video files
  // But for now, let's use a placeholder since we'll extract frames
  return (
    <AbsoluteFill
      style={{
        perspective: `${perspective}px`,
        backgroundColor: "black",
      }}
    >
      <AbsoluteFill
        style={{
          transform: `rotateY(${swivel}deg) rotateX(${tilt}deg) scale(${scale})`,
          transformStyle: "preserve-3d",
          backfaceVisibility: "hidden",
        }}
      >
        <video
          src={videoSrc}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
          muted
          playsInline
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
