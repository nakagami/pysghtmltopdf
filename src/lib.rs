use std::io::Cursor;

use pyo3::exceptions::{PyIOError, PyRuntimeError, PyTimeoutError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sghtmltopdf::{with_render_stack, ConvertError, Converter};

fn to_py_err(err: ConvertError) -> PyErr {
    match err {
        ConvertError::Usage(msg) => PyValueError::new_err(msg),
        ConvertError::Input(msg) => PyIOError::new_err(msg),
        ConvertError::Render(msg) => PyRuntimeError::new_err(msg),
        ConvertError::Timeout(msg) => PyTimeoutError::new_err(msg),
        _ => PyRuntimeError::new_err(err.to_string()),
    }
}

/// Render HTML to PDF bytes.
#[pyfunction]
fn render<'py>(py: Python<'py>, html: &[u8], argv: Vec<String>) -> PyResult<Bound<'py, PyBytes>> {
    let converter = Converter::from_args(argv).map_err(to_py_err)?;
    let html = html.to_vec();

    let pdf_bytes = py
        .detach(move || {
            with_render_stack(move || {
                converter.render_to_vec(Cursor::new(html))
            })
        })
        .map_err(to_py_err)?;

    Ok(PyBytes::new(py, &pdf_bytes))
}

#[pymodule]
fn _sghtmltopdf(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(render, m)?)?;
    Ok(())
}
