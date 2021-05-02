import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import IconButton from '@material-ui/core/IconButton';




export default function Navbar() {


    return (
        <div>
            <AppBar position="static">
                <Toolbar variant="dense">
                    <IconButton edge="start" color="inherit" aria-label="menu">

                    </IconButton>
                    <Typography variant="h6" color="inherit" >
                        <span style={{ marginLeft: "200px" }}>AudioPhile</span>
                    </Typography>
                </Toolbar>
            </AppBar>
        </div>
    );
}