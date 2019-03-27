import React from 'react'
import {withCookies , Cookies} from 'react-cookies'

//import React from 'react';

var csrftoken = Cookies.get('session');

const CSRFToken = () => {
    return (
        <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken} />
    );
};
export default CSRFToken;