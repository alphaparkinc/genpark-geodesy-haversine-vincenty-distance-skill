"""MCP stdio server for Geodesic Distance Engine."""
import sys
import json

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import GeodesyEngine

def handle_rpc(request):
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_distance",
                        "description": "Calculate distance between two coordinates in meters via Haversine or Vincenty formula",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "lat1": {"type": "number"},
                                "lon1": {"type": "number"},
                                "lat2": {"type": "number"},
                                "lon2": {"type": "number"},
                                "method": {"type": "string", "enum": ["haversine", "vincenty"], "default": "vincenty"}
                            },
                            "required": ["lat1", "lon1", "lat2", "lon2"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "calculate_distance":
            lat1 = float(args.get("lat1"))
            lon1 = float(args.get("lon1"))
            lat2 = float(args.get("lat2"))
            lon2 = float(args.get("lon2"))
            m = args.get("method", "vincenty")
            if m == "haversine":
                d = GeodesyEngine.haversine_distance(lat1, lon1, lat2, lon2)
            else:
                d = GeodesyEngine.vincenty_distance(lat1, lon1, lat2, lon2)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"distance_meters": d, "distance_km": round(d / 1000.0, 3)}}
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method {name} not found"}}
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32600, "message": "Invalid request"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_rpc(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32700, "message": str(e)}}) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
