"use client";

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { generateMockData } from "@/lib/utils";
import { ExtendedPost } from "@/types/data";
import { useIntersection } from "@mantine/hooks";

import React, { useEffect, useRef, useState } from "react";

interface PostFeedProps {
  initialHistory: ExtendedPost[];
}

const YourHistoryFeed: React.FC<PostFeedProps> = ({ initialHistory }) => {
  const [history, setHistory] = useState<ExtendedPost[]>(initialHistory);
  const lastPostRef = useRef<HTMLLIElement>(null);
  const { ref, entry } = useIntersection({
    root: lastPostRef.current,
    threshold: 1,
  });

  useEffect(() => {
    if (entry?.isIntersecting) {
      const fetchNextPage = () => {
        const moreData = generateMockData(3); // Example: Generate 10 more mock entries
        setHistory((prevHistory) => [...prevHistory, ...moreData]);
      };
      fetchNextPage(); // Load more posts when the last post comes into view
    }
  }, [entry]);

  return (
    <ul className="space-y-8">
      {history.map((action, index) => (
        <li
          className="flex items-center"
          key={index}
          ref={index === history.length - 1 ? ref : null}
        >
          <Avatar className="h-9 w-9">
            <AvatarImage src={action.avatarSrc} alt="Avatar" />
            <AvatarFallback>{action.avatarFallback}</AvatarFallback>
          </Avatar>
          <div className="ml-4 space-y-1">
            <p className="text-sm font-medium leading-none">{action.title}</p>
            <p className="text-sm text-muted-foreground">{action.date}</p>
          </div>
          <div className="ml-auto font-medium">{action.amount}</div>
        </li>
      ))}
    </ul>
  );
};

export default YourHistoryFeed;
