// types.ts
export type Price = {
  amount: string;
  base: string;
  currency: string;
  timestamp: number;
};

export type ExtendedPost = {
  avatarSrc: string;
  avatarFallback: string;
  title: string;
  date: string;
  amount: string;
};
