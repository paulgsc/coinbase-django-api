"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";

interface UseTabNavigationProps {
  tabParam: string;
  defaultTab: string;
}

const useTabNavigation = ({ tabParam, defaultTab }: UseTabNavigationProps) => {
  const searchParams = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();

  const handleTabClick = (tabId: string) => {
    const newSearchParams = new URLSearchParams(searchParams);
    newSearchParams.set(tabParam, tabId);
    router.push(`${pathname}?${newSearchParams.toString()}`);
  };

  const selectedTab = searchParams.get(tabParam) || defaultTab;

  const isTabActive = (tabId: string) => {
    return selectedTab === tabId;
  };

  return { handleTabClick, isTabActive, selectedTab };
};

export default useTabNavigation;
