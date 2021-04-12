import React from 'react';
import Avatar from '@material-ui/core/Avatar';
import Button from '@material-ui/core/Button';
import CssBaseline from '@material-ui/core/CssBaseline';
import TextField from '@material-ui/core/TextField';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import Checkbox from '@material-ui/core/Checkbox';
import Link from '@material-ui/core/Link';
import Grid from '@material-ui/core/Grid';
import PersonOutlinedIcon from '@material-ui/icons/PersonOutlineOutlined';
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
}));

function Profile() {
  const classes = useStyles();

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <div className={classes.paper}>
        <Avatar className={classes.avatar}>
          <PersonOutlinedIcon />
        </Avatar>
        <Typography component="h1" variant="h5">
          Profile
        </Typography>
        <Grid container direction="column" justify="center" spacing={1} style={{ marginTop: '20px' }}>
          <Grid item>
            <Link href="/update_email" variant="body2">
              Update Email
            </Link>
          </Grid>
          <Grid item>
            <Link href="/update_password" variant="body2">
              Update Password
            </Link>
          </Grid>
          <Grid item style={{ marginTop: '10px' }}>
            <Link href="/delete_account" variant="body2" style={{ color: 'red' }}>
              Delete Account
            </Link>
          </Grid>
        </Grid>
      </div>
    </Container>
  );
}

export default Profile;
