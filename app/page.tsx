// frontend/app/page.tsx
import ChatBox from '../components/ChatBox';

export default function Home() {
  return (
    <div className="container">
      <h1 className="title">RAG Chat Application</h1>
      <p className="description">Enter a URL to scrape content and ask questions!</p>
      <ChatBox />
      <footer className="footer">
        <p>Developed with Next.js, Axios & FastAPI</p>
      </footer>
    </div>
  );
}
