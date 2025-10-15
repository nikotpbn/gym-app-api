import { createContext } from "react";

export const AuthContext = createContext<{
  isLoggedIn: boolean;
  access: string | null;
  refresh: string | null;
  login: (
    access: string,
    refresh: string,
    access_expiration?: Date,
    refresh_expiration?: Date
  ) => void;
  logout: () => void;
}>({
  isLoggedIn: false,
  access: null,
  refresh: null,
  login: () => {},
  logout: () => {},
});
