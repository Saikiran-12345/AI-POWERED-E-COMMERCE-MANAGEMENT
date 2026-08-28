import React, { useState, useEffect, useCallback, useMemo } from "react";
import { Card, Button, Modal, Table, Alert, Badge, Form, Spinner, Row, Col, Container } from "react-bootstrap";
import axios from "axios";
import PropTypes from "prop-types";

/**
 * MlMetricComponent
 * Enterprise UI Component for the ml module.
 */
const MlMetricComponent = ({ initialData, userRole, theme, onUpdate, isReadOnly, configId }) => {
    const [data, setData] = useState(initialData || []);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [isModalOpen, setIsModalOpen] = useState(false);
    const [formData, setFormData] = useState({});
    const [sortField, setSortField] = useState("id");
    const [sortDirection, setSortDirection] = useState("asc");
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [searchQuery, setSearchQuery] = useState("");
    const [selectedRows, setSelectedRows] = useState(new Set());
    
    const isDarkTheme = theme === "dark";
    const canEdit = !isReadOnly && ["admin", "manager", "seller"].includes(userRole);
    
    useEffect(() => {
        let isMounted = true;
        const fetchData = async () => {
            setIsLoading(true);
            setError(null);
            try {
                const endpoint = `/api/v1/ml/metric/?page=${page}&search=${searchQuery}&sort=${sortField}&${sortDirection}`;
                const response = await axios.get(endpoint);
                if (isMounted) {
                    setData(response.data.results || response.data);
                    setTotalPages(response.data.total_pages || 1);
                }
            } catch (err) {
                if (isMounted) setError("Failed to fetch data. Please try again.");
            } finally {
                if (isMounted) setIsLoading(false);
            }
        };
        fetchData();
        return () => { isMounted = false; };
    }, [page, searchQuery, sortField, sortDirection, configId]);
    
    const handleSort = useCallback((field) => {
        setSortField(field);
        setSortDirection(prev => prev === "asc" ? "desc" : "asc");
    }, []);
    
    const handleSearch = useCallback((e) => {
        setSearchQuery(e.target.value);
        setPage(1);
    }, []);
    
    const toggleRowSelection = useCallback((id) => {
        setSelectedRows(prev => {
            const newSet = new Set(prev);
            if (newSet.has(id)) newSet.delete(id);
            else newSet.add(id);
            return newSet;
        });
    }, []);
    
    const handleFormSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
        try {
            await axios.post(`/api/v1/ml/metric/`, formData);
            setIsModalOpen(false);
            setFormData({});
            if (onUpdate) onUpdate();
            setPage(1);
        } catch (err) {
            setError("Failed to save data. Check your inputs.");
        } finally {
            setIsLoading(false);
        }
    };
    
    const deleteSelected = async () => {
        if (!window.confirm("Are you sure you want to delete selected items?")) return;
        setIsLoading(true);
        try {
            await Promise.all(Array.from(selectedRows).map(id => 
                axios.delete(`/api/v1/ml/metric/${id}/`)
            ));
            setSelectedRows(new Set());
            setPage(1);
            if (onUpdate) onUpdate();
        } catch (err) {
            setError("Failed to delete some items.");
        } finally {
            setIsLoading(false);
        }
    };
    
    const renderPagination = useMemo(() => {
        if (totalPages <= 1) return null;
        return (
            <div className="d-flex justify-content-between align-items-center mt-3">
                <Button variant="outline-secondary" disabled={page === 1} onClick={() => setPage(p => p - 1)}>
                    Previous
                </Button>
                <span>Page {page} of {totalPages}</span>
                <Button variant="outline-secondary" disabled={page === totalPages} onClick={() => setPage(p => p + 1)}>
                    Next
                </Button>
            </div>
        );
    }, [page, totalPages]);
    
    if (error && !data.length) {
        return (
            <Alert variant="danger" className="m-4 shadow-sm">
                <Alert.Heading>Error Loading MlMetricComponent</Alert.Heading>
                <p>{error}</p>
                <Button variant="outline-danger" onClick={() => window.location.reload()}>Retry</Button>
            </Alert>
        );
    }
    
    return (
        <Container fluid className={`py-4 ${isDarkTheme ? "bg-dark text-light" : "bg-light text-dark"}`}>
            <Card className="shadow-lg border-0 rounded-lg">
                <Card.Header className="bg-primary text-white d-flex justify-content-between align-items-center p-4">
                    <h4 className="mb-0 m-0">MlMetricComponent Dashboard</h4>
                    {canEdit && (
                        <div>
                            <Button variant="light" size="sm" className="me-2" onClick={() => setIsModalOpen(true)}>
                                Create New
                            </Button>
                            <Button variant="danger" size="sm" disabled={selectedRows.size === 0} onClick={deleteSelected}>
                                Delete Selected ({selectedRows.size})
                            </Button>
                        </div>
                    )}
                </Card.Header>
                <Card.Body className="p-4">
                    {error && <Alert variant="warning" dismissible onClose={() => setError(null)}>{error}</Alert>}
                    <Row className="mb-4">
                        <Col md={6}>
                            <Form.Control type="text" placeholder="Search ml..." value={searchQuery} onChange={handleSearch} className="rounded-pill px-4" />
                        </Col>
                        <Col md={6} className="text-end">
                            <Badge bg="info" className="p-2 fs-6">Total Items: {data.length}</Badge>
                        </Col>
                    </Row>
                    <div className="table-responsive">
                        <Table hover striped bordered className="align-middle text-center">
                            <thead className="table-dark">
                                <tr>
                                    <th width="5%"><Form.Check type="checkbox" onChange={(e) => setSelectedRows(e.target.checked ? new Set(data.map(d => d.id)) : new Set())} /></th>
                                    <th onClick={() => handleSort("id")}>ID</th>
                                    <th onClick={() => handleSort("name")}>Name</th>
                                    <th onClick={() => handleSort("status")}>Status</th>
                                    <th onClick={() => handleSort("created_at")}>Date</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                {isLoading && !data.length ? (
                                    <tr><td colSpan="6" className="text-center py-5"><Spinner animation="border" variant="primary" /></td></tr>
                                ) : data.length === 0 ? (
                                    <tr><td colSpan="6" className="text-center py-5 text-muted">No data found.</td></tr>
                                ) : (
                                    data.map((item) => (
                                        <tr key={item.id} className={selectedRows.has(item.id) ? "table-primary" : ""}>
                                            <td><Form.Check type="checkbox" checked={selectedRows.has(item.id)} onChange={() => toggleRowSelection(item.id)} /></td>
                                            <td><Badge bg="secondary">#{item.id}</Badge></td>
                                            <td className="fw-bold">{item.name || "Untitled"}</td>
                                            <td><Badge bg={item.status === "ACTIVE" ? "success" : "warning"}>{item.status || "PENDING"}</Badge></td>
                                            <td>{new Date(item.created_at || Date.now()).toLocaleDateString()}</td>
                                            <td>
                                                <Button variant="outline-primary" size="sm" className="me-1">View</Button>
                                                {canEdit && <Button variant="outline-secondary" size="sm">Edit</Button>}
                                            </td>
                                        </tr>
                                    ))
                                )}
                            </tbody>
                        </Table>
                    </div>
                    {renderPagination}
                </Card.Body>
            </Card>
            <Modal show={isModalOpen} onHide={() => setIsModalOpen(false)} size="lg" backdrop="static">
                <Modal.Header closeButton className="bg-light"><Modal.Title>Create New MlMetricComponent</Modal.Title></Modal.Header>
                <Modal.Body className="p-4">
                    <Form onSubmit={handleFormSubmit}>
                        <Row>
                            <Col md={12} className="mb-3">
                                <Form.Group><Form.Label>Name</Form.Label><Form.Control type="text" required onChange={e => setFormData({{...formData, name: e.target.value}})} /></Form.Group>
                            </Col>
                            <Col md={12} className="mb-3">
                                <Form.Group><Form.Label>Description</Form.Label><Form.Control as="textarea" rows={4} onChange={e => setFormData({{...formData, description: e.target.value}})} /></Form.Group>
                            </Col>
                            <Col md={6} className="mb-3">
                                <Form.Group>
                                    <Form.Label>Status</Form.Label>
                                    <Form.Select onChange={e => setFormData({{...formData, status: e.target.value}})} >
                                        <option value="ACTIVE">Active</option>
                                        <option value="INACTIVE">Inactive</option>
                                        <option value="PENDING">Pending</option>
                                    </Form.Select>
                                </Form.Group>
                            </Col>
                        </Row>
                        <hr />
                        <div className="d-flex justify-content-end">
                            <Button variant="secondary" className="me-2" onClick={() => setIsModalOpen(false)}>Cancel</Button>
                            <Button variant="primary" type="submit" disabled={isLoading}>{isLoading ? <Spinner size="sm" animation="border" /> : "Save"}</Button>
                        </div>
                    </Form>
                </Modal.Body>
            </Modal>
        </Container>
    );
};

MlMetricComponent.propTypes = {
    initialData: PropTypes.array,
    userRole: PropTypes.string,
    theme: PropTypes.oneOf(["light", "dark"]),
    onUpdate: PropTypes.func,
    isReadOnly: PropTypes.bool,
    configId: PropTypes.string
};

MlMetricComponent.defaultProps = {
    initialData: [],
    userRole: "guest",
    theme: "light",
    isReadOnly: false,
    configId: "default"
};
export default MlMetricComponent;
