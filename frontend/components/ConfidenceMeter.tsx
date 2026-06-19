type ConfidenceMeterProps = {
  value: number;
};

export default function ConfidenceMeter({ value }: ConfidenceMeterProps) {
  const safeValue = Math.max(0, Math.min(value, 100));

  return (
    <div className="meter" aria-label={`Fit score ${safeValue}`}>
      <div className="meter-fill" style={{ width: `${safeValue}%` }} />
    </div>
  );
}
