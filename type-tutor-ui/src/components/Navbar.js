import React from 'react';
import '../styles/App.scss';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography } from '@material-ui/core';

function Navbar() {
  return (
    <AppBar position="static" className="navbar">
      <Toolbar>
        <div className="navbar__left">
          <Typography variant="h3" className="navbar__title">
            TypeTutor
          </Typography>
        </div>
        <div className="navbar__right">
          <Link to="/" style={{ textDecoration: 'none' }}>
            <Typography variant="h6" className="navbar__link">
              Home
            </Typography>
          </Link>
          <Link to="/profile" style={{ textDecoration: 'none' }}>
            <Typography variant="h6" className="navbar__link">
              Profile
            </Typography>
          </Link>
          <Link to="/login" style={{ textDecoration: 'none' }}>
            <Typography variant="h6" className="navbar__link">
              Login
            </Typography>
          </Link>
          <Link to="/register" style={{ textDecoration: 'none' }}>
            <Typography variant="h6" className="navbar__link">
              Register
            </Typography>
          </Link>
        </div>
      </Toolbar>
    </AppBar>
  );
}

export default Navbar;
