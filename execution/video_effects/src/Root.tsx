import React from "react";
import { Composition } from "remotion";
import { Transition3D } from "./Transition3D";

// Demo composition with a test image
export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="Transition3DDemo"
        component={Transition3D}
        durationInFrames={30} // 1 second at 30fps
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          imageSrc: "https://picsum.photos/1920/1080",
          startSwivel: -25,
          startTilt: 12,
          endSwivel: 0,
          endTilt: 0,
          perspective: 1200,
          easeType: "easeOut" as const,
        }}
      />
      <Composition
        id="Transition3DSpring"
        component={Transition3D}
        durationInFrames={45} // 1.5 seconds
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          imageSrc: "https://picsum.photos/1920/1080",
          startSwivel: -35,
          startTilt: 18,
          endSwivel: 0,
          endTilt: 0,
          perspective: 1000,
          easeType: "spring" as const,
        }}
      />
      <Composition
        id="Transition3DSubtle"
        component={Transition3D}
        durationInFrames={20} // Quick 0.67 second
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          imageSrc: "https://picsum.photos/1920/1080",
          startSwivel: -15,
          startTilt: 8,
          endSwivel: 0,
          endTilt: 0,
          perspective: 1500,
          easeType: "easeOut" as const,
        }}
      />
    </>
  );
};
