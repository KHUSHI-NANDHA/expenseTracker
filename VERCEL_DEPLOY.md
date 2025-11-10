# Deploying to Vercel

## Important Notes

⚠️ **SQLite Database Limitation**: SQLite databases on Vercel are stored in `/tmp` which is ephemeral. Data will be lost between deployments or when the serverless function restarts. For production use, consider migrating to:
- Vercel Postgres
- Supabase
- PlanetScale
- Or another cloud database service

## Deployment Steps

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy**:
   ```bash
   vercel
   ```

4. **For production deployment**:
   ```bash
   vercel --prod
   ```

## Environment Variables

Set these in Vercel dashboard (Settings > Environment Variables):

- `GEMINI_API_KEY`: Your Gemini API key
- `SECRET_KEY`: Flask secret key (generate a secure random string)
- `VERCEL`: Set to `1` (already handled in code)

## File Structure

```
expense_tracker/
├── api/
│   └── index.py          # Vercel serverless function handler
├── app.py                # Main Flask application
├── vercel.json           # Vercel configuration
├── requirements.txt      # Python dependencies
└── templates/            # HTML templates
```

## Troubleshooting

- If deployment fails, check Vercel logs
- Make sure all dependencies are in `requirements.txt`
- Ensure `vercel.json` is properly configured
- Check that environment variables are set correctly

