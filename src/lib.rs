use std::io::Cursor;

use pyo3::exceptions::{PyIOError, PyRuntimeError, PyTimeoutError, PyValueError};
use pyo3::prelude::*;
use pyo3::types::PyBytes;
use sghtmltopdf_core::cli::{self, convert, CliError};
use sghtmltopdf_core::render_stack;
use sghtmltopdf_core::sink::MemorySink;

fn to_py_err(err: CliError) -> PyErr {
    match err {
        CliError::Usage(msg) => PyValueError::new_err(msg),
        CliError::Input(msg) => PyIOError::new_err(msg),
        CliError::Render(msg) => PyRuntimeError::new_err(msg),
        CliError::Timeout(msg) => PyTimeoutError::new_err(msg),
    }
}

/// Render HTML to PDF bytes.
#[pyfunction]
fn render<'py>(py: Python<'py>, html: &[u8], argv: Vec<String>) -> PyResult<Bound<'py, PyBytes>> {
    let mut full_argv = Vec::with_capacity(argv.len() + 2);
    full_argv.push("sghtmltopdf".to_string());
    full_argv.push("-".to_string());
    full_argv.extend(argv);

    let (args, fonts) = cli::parse_convert_argv(&full_argv).map_err(to_py_err)?;
    let html = html.to_vec();

    let pdf_bytes = py
        .detach(move || {
            render_stack::with_render_stack(move || {
                convert::render_to_memory(&args, &fonts, Cursor::new(html), MemorySink::new())
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
