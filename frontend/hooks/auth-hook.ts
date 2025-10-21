import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router";

export const useAuth = () => {
  let logoutTimer: ReturnType<typeof setTimeout>;
  let navigate = useNavigate();
  // Access Token is currently set to 5 minutes and
  // refresh Token for 1 day for testing purposes
  const [accessToken, setAccessToken] = useState<string | null>("");
  const [accessTokenExpires, setAccessTokenExpires] = useState<Date | null>();
  const [refreshToken, setRefreshToken] = useState<string | null>("");
  const [subscriptions, setSubscriptions] = useState<string[] | null>([]);

  const login = useCallback(
    (
      access: string,
      refresh: string,
      subscriptions: string[],
      access_expires?: Date,
      refresh_expires?: Date
    ) => {
      // 1000 miliseconds for 1second times 60 for a minute time 5 for 5 minutes
      const access_expiration =
        access_expires || new Date(new Date().getTime() + 1000 * 60 * 60 * 24);
      const refresh_expiration =
        refresh_expires || new Date(new Date().getTime() + 1000 * 60 * 60 * 24 * 2);

      setAccessToken(access);
      setRefreshToken(refresh);
      setSubscriptions(subscriptions);
      setAccessTokenExpires(access_expiration);

      localStorage.setItem(
        "userData",
        JSON.stringify({
          access: access,
          access_expiration: access_expiration.toISOString(),
          refresh: refresh,
          refresh_expiration: refresh_expiration.toISOString(),
          subscriptions: subscriptions,
        })
      );
    },
    []
  );

  const logout = useCallback(() => {
    setAccessToken(null);
    setRefreshToken(null);
    setSubscriptions(null);
    setAccessTokenExpires(null);
    localStorage.removeItem("userData");
    navigate("/login");
  }, []);

  useEffect(() => {
    if (accessToken && accessTokenExpires) {
      const remainingTime = accessTokenExpires.getTime() - new Date().getTime();
      logoutTimer = setTimeout(logout, remainingTime);
    } else {
      clearTimeout(logoutTimer);
    }
  }, [accessToken, logout, accessTokenExpires]);

  useEffect(() => {
    const rawData = localStorage.getItem("userData");
    const storedData = rawData !== null ? JSON.parse(rawData) : null;

    if (storedData) {
      if (storedData.access && storedData.refresh) {
        login(
          storedData.access,
          storedData.refresh,
          storedData.subscriptions,
          new Date(storedData.access_expiration)
        );
      }
    }
  }, [login]);

  return { accessToken, refreshToken, subscriptions, login, logout };
};
