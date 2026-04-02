import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Project Management Frontend",
  description: "Mini project management dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}