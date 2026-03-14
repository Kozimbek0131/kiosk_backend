import { useState } from "react";

/**
 * EmployeePhotoUpload — hodim yoki rahbar rasmi yuklash komponenti
 *
 * Props:
 *   employeeId   — hodim ID si
 *   currentPhoto — mavjud rasm URL (bo'lsa)
 *   onUpdate     — yangi URL bilan chaqiriladigan callback
 *   type         — "employee" yoki "leadership" (default: "employee")
 */
export default function EmployeePhotoUpload({
  employeeId,
  currentPhoto,
  onUpdate,
  type = "employee",
}) {
  const [preview, setPreview] = useState(currentPhoto || null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);

  // API endpoint — type ga qarab
  const getEndpoint = () => {
    if (type === "leadership") {
      return `/api/leadership/${employeeId}/upload-photo/`;
    }
    return `/api/employees/${employeeId}/upload-photo/`;
  };

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    // Fayl hajmini tekshirish (5MB)
    if (file.size > 5 * 1024 * 1024) {
      setError("Rasm hajmi 5MB dan oshmasligi kerak");
      return;
    }

    // Lokal preview — darhol ko'rsatish
    setPreview(URL.createObjectURL(file));
    setLoading(true);
    setError("");
    setSuccess(false);

    const formData = new FormData();
    formData.append("photo", file);

    try {
      const res = await fetch(getEndpoint(), {
        method: "POST",
        body: formData,
      });

      const data = await res.json();

      if (res.ok && data.success) {
        setSuccess(true);
        onUpdate && onUpdate(data.photo_url);
        setTimeout(() => setSuccess(false), 3000);
      } else {
        setError(data.error || "Xatolik yuz berdi");
        setPreview(currentPhoto || null); // Oldingi rasmga qaytish
      }
    } catch (err) {
      setError("Server bilan bog'lanishda xatolik");
      setPreview(currentPhoto || null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      {/* Rasm */}
      <div style={styles.imageWrapper}>
        {preview ? (
          <img src={preview} alt="Hodim rasmi" style={styles.image} />
        ) : (
          <div style={styles.placeholder}>
            <span style={{ fontSize: 40 }}>👤</span>
          </div>
        )}

        {/* Loading overlay */}
        {loading && (
          <div style={styles.overlay}>
            <span style={{ color: "white", fontSize: 24 }}>⏳</span>
          </div>
        )}
      </div>

      {/* Yuklash tugmasi */}
      <label style={{
        ...styles.uploadBtn,
        cursor: loading ? "not-allowed" : "pointer",
        opacity: loading ? 0.7 : 1,
      }}>
        {loading ? "Yuklanmoqda..." : "📷 Rasm yuklash"}
        <input
          type="file"
          accept="image/jpeg,image/png,image/webp"
          onChange={handleFileChange}
          style={{ display: "none" }}
          disabled={loading}
        />
      </label>

      {/* Xatolik xabari */}
      {error && (
        <p style={styles.error}>❌ {error}</p>
      )}

      {/* Muvaffaqiyat xabari */}
      {success && (
        <p style={styles.successMsg}>✅ Rasm saqlandi!</p>
      )}
    </div>
  );
}

const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 10,
  },
  imageWrapper: {
    position: "relative",
    width: 120,
    height: 120,
    borderRadius: "50%",
    overflow: "hidden",
    border: "3px solid #e0e0e0",
    background: "#f5f5f5",
  },
  image: {
    width: "100%",
    height: "100%",
    objectFit: "cover",
  },
  placeholder: {
    width: "100%",
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "#f0f0f0",
  },
  overlay: {
    position: "absolute",
    top: 0, left: 0, right: 0, bottom: 0,
    background: "rgba(0,0,0,0.5)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  },
  uploadBtn: {
    padding: "6px 16px",
    background: "#1890ff",
    color: "white",
    borderRadius: 6,
    fontSize: 13,
    userSelect: "none",
  },
  error: {
    color: "#ff4d4f",
    fontSize: 12,
    margin: 0,
    textAlign: "center",
  },
  successMsg: {
    color: "#52c41a",
    fontSize: 12,
    margin: 0,
  },
};
