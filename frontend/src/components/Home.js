import React from "react";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router";
import { useUserAuth } from "../context/UserAuthContext";
import Main from './main';

const Home = () => {
  const { logOut, user } = useUserAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logOut();
      navigate("/");
    } catch (error) {
      console.log(error.message);
    }
  };

  return (
    <>
      <nav className="bg-white border-gray-200 dark:bg-gray-900">
        <div className="max-w-screen-3xl flex justify-between items-center mx-auto p-4">
          <a href="http://localhost:3000/home" className="flex items-center">
            <h1 className="self-center text-5xl font-semibold whitespace-nowrap dark:text-white">Chatpdf</h1>
          </a>
          <div className="flex items-center space-x-4">
            <span className="text-gray-700 dark:text-gray-200">{user && user.email}</span>
            <Button
              className="bg-blue-500 text-white rounded px-4 py-2"
              onClick={handleLogout}
            >
              Log out
            </Button>
          </div>
        </div>
      </nav>
      <Main />
    </>
  );
};

export default Home;
