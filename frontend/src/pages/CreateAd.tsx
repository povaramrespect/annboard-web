import { useNavigate } from "react-router-dom";
import { AdForm } from "@/components/forms/AdForm";

export default function CreateAd() {
  const navigate = useNavigate();

  return (
    <main className="min-h-screen flex items-center justify-center">
      <AdForm onSuccess={(newAdId) => navigate(`/ads/${newAdId}`)} />
    </main>
  );
}