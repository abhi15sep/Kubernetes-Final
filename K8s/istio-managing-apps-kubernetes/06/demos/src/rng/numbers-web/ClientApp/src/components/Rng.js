import React, { Component } from 'react';

export class Rng extends Component {
  static displayName = Rng.name;

  constructor(props) {
    super(props);
    this.state = { randomNumber: -1, error: null };
    this.getRandomNumber = this.getRandomNumber.bind(this);
  }

  async getRandomNumber() {
    try {
      const response = await fetch('rng');
      const data = await response.json();
      this.setState({ randomNumber: data, error: null });
    }
    catch (err) {
      this.setState({ randomNumber: -1, error: err });
    }
  }

  render() {
    let contents = this.state.randomNumber > -1
      ? <p aria-live="polite">Here it is: <strong>{this.state.randomNumber}</strong></p>
      : this.state.error
        ? <p><strong>RNG service call failed!</strong></p>
        : <p></p>

    return (
      <div>
        <h1>RNG</h1>
        <button className="btn btn-primary" onClick={this.getRandomNumber}>Get Random Number!</button>
        <p/>
        {contents}
      </div>
    );
  }
}
