"use client";
import { SessionProvider } from "next-auth/react";

export function NextAuthProvider({ children }: { children: React.ReactNode }) {
  const basePath = (process.env.NEXT_PUBLIC_BASE_PATH ?? "").replace(/\/$/, "");
  return <SessionProvider basePath={`${basePath}/api/auth`}>{children}</SessionProvider>;
}
