"""Automated evidence generation script utilizing Playwright."""

import asyncio
import os
import shutil
import sys
from pathlib import Path

import httpx

# Configure sys.path for workspace imports
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT))


async def verify_backend_health() -> None:
    """Check FastAPI backend endpoint liveness."""
    url = "http://127.0.0.1:8000/health"
    print(f"Checking backend liveness at: {url}...")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=5)
            if response.status_code == 200:
                print("FastAPI Backend is healthy.")
                return
            raise RuntimeError(f"Backend returned HTTP {response.status_code}")
    except Exception as exc:
        raise RuntimeError(f"Failed to connect to backend: {exc}") from exc


async def run_evidence_pipeline() -> None:
    """Execute Playwright browser actions to capture evidence screenshots and videos."""
    from playwright.async_api import async_playwright

    # Ensure directories exist
    screenshots_dir = PROJECT_ROOT / "docs" / "screenshots"
    video_dir = PROJECT_ROOT / "demo" / "raw"
    screenshots_dir.mkdir(parents=True, exist_ok=True)
    video_dir.mkdir(parents=True, exist_ok=True)

    print("Verifying backend health...")
    await verify_backend_health()

    print("Starting Playwright browser...")
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        # Configure video recording
        context = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 720},
        )
        page = await context.new_page()

        # 1. Open Dashboard Home
        print("Navigating to Streamlit Dashboard Home...")
        await page.goto("http://127.0.0.1:8501")
        await page.wait_for_timeout(3000)  # Wait for load
        await page.screenshot(path=str(screenshots_dir / "dashboard_home.png"))
        print("Captured Dashboard Home.")

        # 2. Go to Ingest & Audit tab
        print("Navigating to Ingest & Audit Tab...")
        await page.click("text=Ingest & Audit")
        await page.wait_for_timeout(2000)

        # Fill run ID
        await page.fill("input[aria-label='Invoice Run ID']", "inv-audit-demo-001")
        # Upload clean sample invoice
        sample_invoice_path = PROJECT_ROOT / "example_invoice.txt"
        if not sample_invoice_path.exists():
            raise FileNotFoundError(f"Missing sample invoice file: {sample_invoice_path}")

        print("Uploading sample invoice...")
        await page.set_input_files("input[type=file]", str(sample_invoice_path))
        await page.wait_for_timeout(2000)
        await page.screenshot(path=str(screenshots_dir / "upload_page.png"))
        print("Captured Upload Page.")

        # Click audit trigger button
        print("Running Compliance Audit...")
        await page.click("button:has-text('Run Compliance Audit')")
        # Take a screenshot during processing
        await page.wait_for_timeout(1000)
        await page.screenshot(path=str(screenshots_dir / "processing_stage.png"))
        print("Captured Processing Stage.")

        # Wait for audit run success completion
        print("Waiting for audit completion...")
        await page.wait_for_selector("text=Audit Run completed successfully!", timeout=30000)
        await page.wait_for_timeout(2000)

        # Capture findings, score, and reports
        await page.screenshot(path=str(screenshots_dir / "findings_stage.png"))
        print("Captured Findings details.")

        # Scroll to score card metrics
        await page.screenshot(path=str(screenshots_dir / "risk_scoring.png"))
        print("Captured Risk scorecard.")

        # Capture Markdown report section
        await page.screenshot(path=str(screenshots_dir / "markdown_report.png"))
        print("Captured Markdown Report.")

        # 3. Open Swagger API docs
        print("Navigating to Swagger API documentation...")
        await page.goto("http://127.0.0.1:8000/docs")
        await page.wait_for_timeout(3000)
        await page.screenshot(path=str(screenshots_dir / "swagger_docs.png"))
        print("Captured Swagger Docs.")

        # Clean context and extract video path
        video_path = await page.video.path() if page.video else None
        await context.close()
        await browser.close()

        # Rename recorded video to a clean target path
        if video_path and os.path.exists(video_path):
            shutil.copy(video_path, str(video_dir / "demo_walkthrough.webm"))
            print(f"Saved walkthrough video: {video_dir / 'demo_walkthrough.webm'}")

    # 4. Generate screenshots index markdown
    print("Generating docs/screenshots/index.md...")
    index_md = screenshots_dir / "index.md"
    index_md.write_text(
        """# 📸 VoltAudit AI Demo Screenshots Gallery

This gallery details the visual interfaces and execution results
captured during local application startup audits.

---

## 1. Dashboard Home
![Dashboard Home](dashboard_home.png)
*Overview of electricity utility audits and compliance score metrics.*

---

## 2. Ingest & Upload Page
![Upload Page](upload_page.png)
*Invoice run registration form and text/pdf document uploader.*

---

## 3. Ingress Processing Stage
![Processing Stage](processing_stage.png)
*Cooperative AI Workforce progress bar updating live as specialists execute skills.*

---

## 4. Audit Findings
![Findings Details](findings_stage.png)
*Compilation of prices, physical generation meter variances, and double-billing duplicate runs.*

---

## 5. Risk Scorecard
![Risk Scorecard](risk_scoring.png)
*Final compliance score calculation showing deduction rules applied.*

---

## 6. Markdown Explainers Report
![Narrative Report](markdown_report.png)
*Generated audit narrative log summarizing findings.*

---

## 7. Swagger REST API Documentation
![Swagger API docs](swagger_docs.png)
*FastAPI REST gateway contracts supporting interactive developer checks.*
""",
        encoding="utf-8",
    )
    print("Screenshots index file successfully generated.")


if __name__ == "__main__":
    try:
        asyncio.run(run_evidence_pipeline())
        sys.exit(0)
    except Exception as error:
        print(f"❌ Evidence generation failed: {error}", file=sys.stderr)
        sys.exit(1)
