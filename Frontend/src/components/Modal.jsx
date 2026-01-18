export default function Modal({ open, onClose, children }) {
  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white w-full max-w-3xl  rounded-lg p-6 h-screen relative  overflow-y-scroll">
        <button
          onClick={onClose}
          className="absolute top-3 right-3 text-gray-500"
        >
          ✕
        </button>
        {children}
      </div>
    </div>
  );
}
