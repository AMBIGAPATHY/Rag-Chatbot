// frontend/app/layout.tsx
import './globals.css';

export const metadata = {
  title: 'RAG Chat Application',
  description: 'RAG Chat App using Next.js & FastAPI',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
