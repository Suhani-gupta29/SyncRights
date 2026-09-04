import "./globals.css";

export const metadata = {
  title: "SyncRights",
  description: "Music Rights & Compliance Intelligence",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>{children}</body>
    </html>
  );
}