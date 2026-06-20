type ConfidenceMeterProps = {
  value: number;
  reasons?: string[];
};

/**
 * Visualizes CONFIDENCE (how sure the system is), not the fit score.
 * This is intentionally a separate component from the fit score bar —
 * EVIDIQ's whole premise is that these two numbers must never be
 * visually conflated. See backend/services/confidence/confidence_engine.py
 * for how this value is actually computed.
 */
function confidenceTier(value: number): "low" | "medium" | "high" {
  if (value < 40) return "low";
  if (value < 70) return "medium";
  return "high";
}

export default function ConfidenceMeter({ value, reasons = [] }: ConfidenceMeterProps) {
  const safeValue = Math.max(0, Math.min(value, 100));
  const tier = confidenceTier(safeValue);

  return (
    <div className="confidence-block">
      <div
        className={`confidence-meter confidence-${tier}`}
        aria-label={`Confidence ${safeValue} percent`}
      >
        <div className="confidence-fill" style={{ width: `${safeValue}%` }} />
      </div>
      <span className="confidence-label">Confidence: {safeValue}</span>

      {reasons.length > 0 && (
        <ul className="confidence-reasons">
          {reasons.map((reason) => (
            <li key={reason}>{reason}</li>
          ))}
        </ul>
      )}
    </div>
  );
}