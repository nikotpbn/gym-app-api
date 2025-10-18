import { createContext } from "react";

export const AuthContext = createContext<{
  isLoggedIn: boolean | null;
  access: string | null;
  refresh: string | null;
  subscriptions: string[] | null;
  login: (
    access: string,
    refresh: string,
    subscriptions: string[],
    access_expiration?: Date,
    refresh_expiration?: Date
  ) => void;
  logout: () => void;
}>({
  isLoggedIn: false,
  access: null,
  refresh: null,
  subscriptions: null,
  login: () => {},
  logout: () => {},
});
