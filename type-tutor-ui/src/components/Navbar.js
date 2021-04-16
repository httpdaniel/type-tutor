import React, { useState } from 'react';
import '../styles/App.scss';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Typography } from '@material-ui/core';

function Navbar() {
  const [jwt, setJwt] = useState(localStorage.getItem('jwt'));
  const [email, setEmail] = useState(localStorage.getItem('email'));

  React.useEffect(() => {
    window.addEventListener('storage', () => {
      console.log('Storage Update');
      setJwt(localStorage.getItem('jwt'));
      setEmail(localStorage.getItem('email'));
    });
  }, []);

  function handleLogout() {
    localStorage.removeItem('jwt');
    setJwt(localStorage.getItem('jwt'));
    localStorage.removeItem('email');
    setJwt(localStorage.getItem('email'));
    window.location.href = '/login';
  }

  if (jwt) {
    return (
      <AppBar position="static" className="navbar" style={{ background: '#eeeeee' }}>
        <Toolbar>
          <div className="navbar__left">
            <Typography variant="h3" className="navbar__title">
              TypeTutor
            </Typography>
            <Typography variant="h6" className="navbar__title" style={{ marginLeft: '30px' }}>
              Typing as:
              <br />
              { email }
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
            {/* <Link to="/visualization" style={{ textDecoration: 'none' }}>
              <Typography variant="h6" className="navbar__link">
                Statistics
              </Typography>
            </Link> */}
            <button type="button" onClick={() => handleLogout()} style={{ textDecoration: 'none', border: 'none', cursor: 'pointer' }}>
              <Typography variant="h6" className="navbar__link">
                Logout
              </Typography>
            </button>
          </div>
        </Toolbar>
      </AppBar>
    );
  }

  return (
    <AppBar position="static" className="navbar" style={{ background: '#eeeeee' }}>
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
          <Link to="/visualization" style={{ textDecoration: 'none' }}>
            <Typography variant="h6" className="navbar__link">
              Statistics
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
