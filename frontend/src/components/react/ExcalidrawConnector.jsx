import React from 'react';
import { createRoot } from 'react-dom/client';
import ExcalidrawWrapper from './Excalidraw';

export class ExcalidrawConnector {
  constructor(targetEl) {
    this.targetEl = targetEl;
    this.root = createRoot(targetEl);
  }

  render() {
    this.root.render(<ExcalidrawWrapper />);
  }
}
