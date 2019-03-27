import axios from 'axios'
//import cookie from 'react-cookie'




export const register = newUser => {
    return axios
    .post('/users/register', {
        first_name: newUser.first_name,
        last_name: newUser.last_name,
        email: newUser.email,
        username: newUser.username,
        password: newUser.password
    })
    .then(response =>{
        console.log('registered')
    })
}

export const login = user => {
    return axios.post('users/login',{
        username: user.username,
        password: user.pasword

    })
    .then(res=> {
        localStorage.setItem('token', res.data.token)
        return res.data
    })
    .catch(err => {
        console.log(err)
    })
}

export const remove = user => {
    return axios.post('/delete',{
        username: user.username,
        

    })
    .then(res=> {
        localStorage.setItem('token', res.data.token)
        return res.data
    })
    .catch(err => {
        console.log(err)
    })
}

