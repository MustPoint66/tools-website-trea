import React from "react";
import { GlowingEffect } from "./glowing-effect";

interface ToolCardProps {
  icon: JSX.Element;
  title: string;
  description: string;
  tags: string[];
  isFeatured?: boolean;
  onClick: () => void;
}

const ToolCard: React.FC<ToolCardProps> = ({
  icon,
  title,
  description,
  tags,
  isFeatured = false,
  onClick,
}) => {
  return (
    <div
      className="group relative rounded-xl border transition-transform hover:scale-105"
      onClick={onClick}
    >
      <GlowingEffect
        glow={true}
        className="absolute -inset-px opacity-0 group-hover:opacity-100"
        spread={30}
        blur={5}
        proximity={40}
        borderWidth={2}
      />
      <div className="flex flex-col items-center p-4 space-y-2">
        <div className="text-6xl">{icon}</div>
        <h3 className="text-lg font-semibold text-center">
          {title} {isFeatured && <span className="ml-2 text-xs p-1 bg-yellow-300 rounded">Featured</span>}
        </h3>
        <p className="text-center text-gray-700">{description}</p>
        <div className="flex flex-wrap justify-center mt-2">
          {tags.map((tag) => (
            <span key={tag} className="text-xs m-1 p-1 bg-gray-200 rounded">
              {tag}
            </span>
          ))}
        </div>
      </div>
      <button
        className="w-full py-2 mt-4 text-center bg-blue-500 text-white rounded-b-xl hover:bg-blue-600"
      >
        Use Tool
      </button>
    </div>
  );
};

export { ToolCard };

