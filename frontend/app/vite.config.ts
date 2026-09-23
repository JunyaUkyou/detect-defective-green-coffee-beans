import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  server: {
    host: true,
  },
  plugins: [react()],
  // プレビューサーバーの設定（本番 ECS 用）
  preview: {
    host: "0.0.0.0",
    port: 5173,
    allowedHosts: true, // ★ ALB からのアクセス・ヘルスチェックをすべて許可する
  },
});
