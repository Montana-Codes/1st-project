# 1st-project

Browser-based side-by-side New Testament reader with:

- **NIV** column (left)
- **Chinese Union Version (CUV)** column (right)
- Book/chapter selector + previous/next chapter controls
- Synchronized scrolling toggle (on/off)
- Local **PDF/EPUB** import for each translation

## Run locally

This project is static HTML/CSS/JS. You can open `Index.html` directly, but using a local server is recommended:

```bash
cd 1st-project
python3 -m http.server 8000
```

Then open `http://localhost:8000/Index.html`.

## How to load Bible files

1. Prepare your **legally obtained** New Testament files:
   - NIV file (PDF or EPUB)
   - CUV file (PDF or EPUB)
2. In the app, use the NIV and CUV file pickers.
3. Select book/chapter and read side-by-side.

## Notes and limitations

- This repository does **not** include NIV/CUV text and does not redistribute copyrighted Bible content.
- Files are parsed **locally in your browser** and are not uploaded by this app.
- PDF/EPUB chapter boundaries vary by publisher layout, so chapter navigation is best-effort for imported files.
