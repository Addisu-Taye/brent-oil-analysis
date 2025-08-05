export default function IndicatorCard({ title, value, subtitle }: { title: string, value: string | number, subtitle?: string }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-md border border-gray-200">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <h3 className="text-2xl font-bold text-gray-900 mt-1">{value}</h3>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
      </div>
    </div>
  );
}