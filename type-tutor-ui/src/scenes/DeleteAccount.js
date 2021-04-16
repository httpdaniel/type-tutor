/* eslint-disable*/
import React, { useState }  from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import LockOutlinedIcon from '@material-ui/icons/LockOutlined';
import Typography from '@material-ui/core/Typography';
import { makeStyles } from '@material-ui/core/styles';
import Container from '@material-ui/core/Container';


const useStyles = makeStyles((theme) => ({
  paper: {
    marginTop: theme.spacing(8),
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
  },
  avatar: {
    margin: theme.spacing(1),
    backgroundColor: theme.palette.secondary.main,
  },
  form: {
    width: '100%', // Fix IE 11 issue.
    marginTop: theme.spacing(1),
  },
  submit: {
    margin: theme.spacing(3, 0, 2),
  },
}));

function UpdatePassword() {
  const classes = useStyles();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorText, setErrorText] = useState('');

  function handleSubmit(event) {
    let error = false
    event.preventDefault();
    fetch('/delete_account', {
      method: 'DELETE',
      headers: {
        'Content-type': 'application/json',
      },
      body: JSON.stringify({email: email, password: password, token: localStorage.getItem('jwt') || ''}),
    })
    .then(res => {
      error = !res.ok
      console.log(res)
      return res.json()
    })
    .then(
      (res) => {
        console.log(res)
        let str = JSON.stringify(res)
        str = str.substring(12, str.length - 2)
        if(error)
        {
          setErrorText(str)
        }
        else
        {
          setErrorText('')
          localStorage.removeItem('jwt');
          localStorage.removeItem('email');
          window.location.href = "/";
        }
      }); 
  }

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <LockOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Delete account
        </Typography>
        <Typography component="h3" variant="h6" style={{color: "red"}}>
          {errorText}
        </Typography>
        <form className={classes.form} noValidate onSubmit={handleSubmit}>
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            id="email"
            label="Email Address"
            name="email"
            autoComplete="email"
            autoFocus
            value={email}
            onInput={ e=>setEmail(e.target.value)}
          />
          <TextField
            variant="outlined"
            margin="normal"
            required
            fullWidth
            name="password"
            label="Password"
            type="password"
            id="password"
            value={password}
            onInput={ e=>setPassword(e.target.value)}
          />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            style={{backgroundColor: "red", color: "white" }}
            className={classes.submit}
          >
            Delete Account
          </Button>
        </form>
      </div>
    </Container>
    //<div>
    //  <h1>This is the login page.</h1>
    //</div>
    
  );
}

export default UpdatePassword;
