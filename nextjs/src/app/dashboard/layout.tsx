import { cn, constructMetadata } from "@/lib/utils";

export const metadata = constructMetadata({
  title: "Dashboard",
  description: "view charts",
});

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="relative flex flex-col min-h-screen">
      <div className="flex-grow flex-1">{children}</div>
    </main>
  );
}
