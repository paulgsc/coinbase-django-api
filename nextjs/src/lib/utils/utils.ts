import { ExtendedPost } from "@/types/data";
import { type ClassValue, clsx } from "clsx";
import { Metadata } from "next";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function constructMetadata({
  title = "DigitalHippo - the marketplace for digital assets",
  description = "DigitalHippo is an open-source marketplace for high-quality digital goods.",
  image = "/thumbnail.png",
  icons = "/favicon.ico",
  noIndex = false,
}: {
  title?: string;
  description?: string;
  image?: string;
  icons?: string;
  noIndex?: boolean;
} = {}): Metadata {
  return {
    title,
    description,
    openGraph: {
      title,
      description,
      images: [
        {
          url: image,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title,
      description,
      images: [image],
      creator: "@joshtriedcoding",
    },
    icons,
    metadataBase: new URL("https://digitalhippo.up.railway.app"),
    ...(noIndex && {
      robots: {
        index: false,
        follow: false,
      },
    }),
  };
}

export const generateMockData = (count: number): ExtendedPost[] => {
  // Generate mock data
  const newData: ExtendedPost[] = [];
  for (let i = 0; i < count; i++) {
    // Create mock entries
    const newEntry: ExtendedPost = {
      avatarSrc: "/avatars/placeholder.png",
      avatarFallback: "Placeholder",
      title: `New Entry ${i}`,
      date: new Date().toLocaleDateString(),
      amount: "100", // Example amount
    };
    newData.push(newEntry);
  }
  return newData;
};
