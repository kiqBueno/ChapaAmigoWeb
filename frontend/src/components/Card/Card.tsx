import "./Card.css";

const Card = ({ title, content }: { title: string; content: string }) => (
  <div className="card">
    <h2>{title}</h2>
    <p>{content}</p>
  </div>
);

export default Card;
