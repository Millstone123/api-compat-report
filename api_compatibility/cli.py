from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import compare_documents, review_document, validate_sample
from .report import render_report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="api-compat-report")
    sub = parser.add_subparsers(dest="command", required=True)
    compare = sub.add_parser("compare")
    compare.add_argument("--from", dest="before", required=True)
    compare.add_argument("--to", dest="after", required=True)
    validate = sub.add_parser("validate")
    validate.add_argument("sample")
    validate.add_argument("--schema", required=True)
    report = sub.add_parser("report")
    report.add_argument("before")
    report.add_argument("after")
    report.add_argument("--output", required=True)
    review = sub.add_parser("review")
    review.add_argument("schema")
    diagnose = sub.add_parser("diagnose")
    diagnose.add_argument("--from", dest="before", required=True)
    diagnose.add_argument("--to", dest="after", required=True)
    args = parser.parse_args(argv)
    if args.command == "compare":
        result = compare_documents(args.before, args.after)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0
    if args.command == "validate":
        result = validate_sample(args.sample, args.schema)
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["valid"] else 1
    if args.command == "report":
        result = compare_documents(args.before, args.after)
        Path(args.output).write_text(render_report(result, args.before, args.after), encoding="utf-8")
        print("wrote %s" % args.output)
        return 0
    if args.command == "review":
        print(json.dumps(review_document(args.schema), indent=2, sort_keys=True))
        return 0
    result = compare_documents(args.before, args.after)
    print("diagnostic=%s changes=%d" % ("compatible" if result.get("valid") else "invalid", len(result.get("changes", []))))
    return 0
