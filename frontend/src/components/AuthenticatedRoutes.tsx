import { Outlet } from "react-router-dom";
import RequireAuth from "../context/require-auth";

const AuthenticatedRoutes = () => {
  return (
    <RequireAuth>
      <Outlet />
    </RequireAuth>
  );
};

export default AuthenticatedRoutes;
