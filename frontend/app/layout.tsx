import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/layout/Sidebar";
import { ReactQueryProvider } from "@/providers/ReactQueryProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Agentic Watch Dashboard",
  description: "AI Governance Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} flex overflow-hidden h-screen`}>
        <ReactQueryProvider>
          <Sidebar />
          <main className="flex-1 overflow-y-auto bg-gray-50">
            <div className="p-8 max-w-7xl mx-auto">
              {children}
            </div>
          </main>
        </ReactQueryProvider>
      </body>
    </html>
  );
}
