import { Badge } from "./ui/badge";

const TRADE_CODES = {
  "03": "Concrete",
  "04": "Masonry",
  "05": "Metals",
  "06": "Wood/Plastics",
  "07": "Thermal/Moisture",
  "08": "Openings",
  "09": "Finishes",
  "10": "Specialties",
  "22": "Plumbing",
  "23": "HVAC",
  "26": "Electrical",
  "31": "Earthwork",
  "32": "Exterior"
};

export function TradeBadge({ code, showCode = true }) {
  const name = TRADE_CODES[code] || code;
  
  return (
    <Badge 
      variant="outline" 
      className={`trade-badge-${code} text-xs font-medium`}
      data-testid={`trade-badge-${code}`}
    >
      {showCode ? `${code} - ${name}` : name}
    </Badge>
  );
}

export function getTradeCodeName(code) {
  return TRADE_CODES[code] || code;
}

export { TRADE_CODES };
