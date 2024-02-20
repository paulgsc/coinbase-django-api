// types.ts
export type Price = {
  amount: string;
  base: string;
  currency: string;
  timestamp: number;
  symbol: string;
  full_name: string;
};

export type ExtendedPost = {
  avatarSrc: string;
  avatarFallback: string;
  title: string;
  date: string;
  amount: string;
};
