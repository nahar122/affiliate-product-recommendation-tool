import { Link, useNavigate } from "react-router-dom";

export default function BaseNavbar() {
  const navigate = useNavigate();
  return (
    <div className="navbar bg-base-100 shadow-md">
      <div className="navbar-start">
        <div className="dropdown">
          <div
            tabIndex={0}
            role="button"
            className="btn lg:hidden"
            onClick={() => navigate("/")}
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M4 6h16M4 12h8m-8 6h16"
              />
            </svg>
          </div>
          <ul
            tabIndex={0}
            className="menu menu-sm dropdown-content mt-3 z-[1] p-2 shadow bg-base-100 rounded-box w-52"
          >
            <li>
              <a onClick={() => navigate("/")}>About</a>
            </li>
          </ul>
        </div>
        <a
          className="btn bg-neutral text-white text-xl"
          onClick={() => navigate("/")}
        >
          AffliateMe
        </a>
      </div>
      <div className="navbar-center hidden lg:flex">
        <ul className="menu font-semibold menu-horizontal px-1">
          <li>
            <a onClick={() => navigate("/about")}>About</a>
          </li>
        </ul>
      </div>
      <div className="navbar-end">
        <Link to="/login">
          <button className="btn btn-neutral text-white hover:bg-base-300 hover:text-black hover:border-none">
            Sign In
          </button>
        </Link>
      </div>
    </div>
  );
}
