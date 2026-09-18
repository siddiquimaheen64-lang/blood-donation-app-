# LifeLink Backend

Node.js + Express + TypeScript + MongoDB API for the LifeLink mobile app.

## 1. Install
```bash
npm install
```

## 2. Environment
Copy `.env.example` to `.env` and set `MONGO_URI` and `JWT_SECRET`.

For local MongoDB:
```env
MONGO_URI=mongodb://127.0.0.1:27017/lifelink
PORT=5000
JWT_SECRET=replace-with-a-long-secret
CLIENT_ORIGIN=*
```

## 3. Run
```bash
npm run dev
```

Build/production:
```bash
npm run build
npm start
```

Optional demo data:
```bash
npm run seed
```
Demo accounts use password `123456`.

## Main API endpoints
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET/PATCH /api/users/me`
- `GET /api/dashboard`
- `GET /api/requests`
- `GET /api/requests/open`
- `POST /api/requests`
- `PATCH /api/requests/:id/status`
- `GET /api/donations/mine`
- `POST /api/donations`
- `GET /api/inventory`
- `PUT /api/inventory`
- `GET /api/notifications`
- `PATCH /api/notifications/:id/read`

Use `Authorization: Bearer <token>` for protected endpoints.

## Mobile app connection
Create one API helper in the Expo app and use your computer's LAN IP on a physical phone, for example:
`http://192.168.1.10:5000/api`
Do not use `localhost` from a physical phone; `localhost` points to the phone itself.
