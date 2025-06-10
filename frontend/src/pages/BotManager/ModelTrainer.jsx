export default function ModelTrainer({ status, onTrain }) {
  return (
    <div className="my-4 p-4 bg-gray-100 rounded">
      <button 
        onClick={onTrain}
        className="bg-blue-500 text-white px-4 py-2 rounded"
      >
        Entrenar Modelo NLP
      </button>
      {status && <p className="mt-2">{status}</p>}
    </div>
  );
}