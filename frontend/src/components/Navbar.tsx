import AuthNavbar from "./AuthNavbar";
import BaseNavbar from "./BaseNavbar";
import { useContext } from "react";
import { AuthContext } from "../context/auth-context";

const Navbar = () => {
  const { currentUser } = useContext(AuthContext);

  if (currentUser) {
    return <AuthNavbar />;
  } else {
    return <BaseNavbar />;
  }
};

export default Navbar;
