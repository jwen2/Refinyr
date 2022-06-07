import React from "react";
import "./Header.css";

const Header = () => {
  return (
    <div className="headerContainer">
      <nav className="header">
        <h3>Refiner</h3>

        <ul className="menu">
          <li className="menuItems">Home</li>
          <li className="menuItems">About</li>
          <li className="menuItems">Roadmap</li>
          <li className="menuItems">Showcase</li>
          <li className="menuItems">Team</li>
        </ul>

        <button className="headerButton" link="https://google.com">
          Contact Us
        </button>
      </nav>
    </div>
  );
};

export default Header;
