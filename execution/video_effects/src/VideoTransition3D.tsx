import React from "react";
import {
  AbsoluteFill,
  Sequence,
  Img,
  interpolate,
  useCurrentFrame,
  useVideoConfig,
  spring,
  Easing,
  staticFile,
  getInputProps,
} from "remotion";

// This component takes an image sequence (frames extracted from video)
// and applies a 3D pan transition effect

interface VideoTransition3DProps {
  frameCount: number;
  frameDir: string; // Directory containing frame_%04d.jpg
  startSwivel: number;
  startTilt: number;
  endSwivel: number;
  endTilt: number;
  perspective: number;
  playbackRate: number; // e.g., 7 for 700% speed
}

export const VideoTransition3D: React.FC<VideoTransition3DProps> = ({
  frameCount,
  frameDir,
  startSwivel = -30,
  startTilt = 15,
  endSwivel = 0,
  endTilt = 0,
  perspective = 1000,
  playbackRate = 7,
}) => {
  const frame = useCurrentFrame();
  const { durationInFrames, fps } = useVideoConfig();

  // Calculate which source frame to show (accounting for speed-up)
  const sourceFrameIndex = Math.min(
    Math.floor(frame * playbackRate),
    frameCount - 1
  );

  // Progress for the 3D effect (0 to 1 over the duration)
  const progress = interpolate(frame, [0, durationInFrames], [0, 1], {
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });

  // Interpolate rotation values
  const swivel = interpolate(progress, [0, 1], [startSwivel, endSwivel]);
  const tilt = interpolate(progress, [0, 1], [startTilt, endTilt]);
  const scale = interpolate(progress, [0, 1], [1.15, 1]);

  // Frame filename (zero-padded)
  const frameFilename = `frame_${String(sourceFrameIndex).padStart(4, "0")}.jpg`;
  const framePath = staticFile(`${frameDir}/${frameFilename}`);

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
          src={framePath}
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

// Dynamic version that reads props from input
export const VideoTransition3DDynamic: React.FC = () => {
  const props = getInputProps() as VideoTransition3DProps;
  return <VideoTransition3D {...props} />;
};
