import React, {Component} from 'react'

class Found extends Component{
    constructor(){
        super()
        this.state ={
            username: '',
            
        
            errors: {}
            
        }
    }
    

    
    render(){
        return(
            <div className = "container">
            <div className = "jumbotron mt-5">
            <div className = "col-sm-8 mt-5">
            <h1 className ="text-center">
            
            </h1>
            </div>
            <table className = "table col-md-6 mx-auto">
            <tbody>
                
                <tr>
                    <td>Username</td>
                    <td>{this.state.items}</td>
                </tr>
               
                
                
            </tbody>
            </table>
            </div>
            </div>
        )
    }
    
}

export default Found