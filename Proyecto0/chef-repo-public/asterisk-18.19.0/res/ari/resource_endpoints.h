/*
 * Asterisk -- An open source telephony toolkit.
 *
 * Copyright (C) 2012 - 2013, Digium, Inc.
 *
 * David M. Lee, II <dlee@digium.com>
 *
 * See http://www.asterisk.org for more information about
 * the Asterisk project. Please do not directly contact
 * any of the maintainers of this project for assistance;
 * the project provides a web site, mailing lists and IRC
 * channels for your use.
 *
 * This program is free software, distributed under the terms of
 * the GNU General Public License Version 2. See the LICENSE file
 * at the top of the source tree.
 */

/*! \file
 *
 * \brief Generated file - declares stubs to be implemented in
 * res/ari/resource_endpoints.c
 *
 * Endpoint resources
 *
 * \author David M. Lee, II <dlee@digium.com>
 */

/*
 * !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 * !!!!!                               DO NOT EDIT                        !!!!!
 * !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 * This file is generated by a mustache template. Please see the original
 * template in rest-api-templates/ari_resource.h.mustache
 */

#ifndef _ASTERISK_RESOURCE_ENDPOINTS_H
#define _ASTERISK_RESOURCE_ENDPOINTS_H

#include "asterisk/ari.h"

/*! Argument struct for ast_ari_endpoints_list() */
struct ast_ari_endpoints_list_args {
};
/*!
 * \brief List all endpoints.
 *
 * \param headers HTTP headers
 * \param args Swagger parameters
 * \param[out] response HTTP response
 */
void ast_ari_endpoints_list(struct ast_variable *headers, struct ast_ari_endpoints_list_args *args, struct ast_ari_response *response);
/*! Argument struct for ast_ari_endpoints_send_message() */
struct ast_ari_endpoints_send_message_args {
	/*! The endpoint resource or technology specific URI to send the message to. Valid resources are sip, pjsip, and xmpp. */
	const char *to;
	/*! The endpoint resource or technology specific identity to send this message from. Valid resources are sip, pjsip, and xmpp. */
	const char *from;
	/*! The body of the message */
	const char *body;
	struct ast_json *variables;
};
/*!
 * \brief Body parsing function for /endpoints/sendMessage.
 * \param body The JSON body from which to parse parameters.
 * \param[out] args The args structure to parse into.
 * \retval zero on success
 * \retval non-zero on failure
 */
int ast_ari_endpoints_send_message_parse_body(
	struct ast_json *body,
	struct ast_ari_endpoints_send_message_args *args);

/*!
 * \brief Send a message to some technology URI or endpoint.
 *
 * \param headers HTTP headers
 * \param args Swagger parameters
 * \param[out] response HTTP response
 */
void ast_ari_endpoints_send_message(struct ast_variable *headers, struct ast_ari_endpoints_send_message_args *args, struct ast_ari_response *response);
/*! Argument struct for ast_ari_endpoints_list_by_tech() */
struct ast_ari_endpoints_list_by_tech_args {
	/*! Technology of the endpoints (sip,iax2,...) */
	const char *tech;
};
/*!
 * \brief List available endoints for a given endpoint technology.
 *
 * \param headers HTTP headers
 * \param args Swagger parameters
 * \param[out] response HTTP response
 */
void ast_ari_endpoints_list_by_tech(struct ast_variable *headers, struct ast_ari_endpoints_list_by_tech_args *args, struct ast_ari_response *response);
/*! Argument struct for ast_ari_endpoints_get() */
struct ast_ari_endpoints_get_args {
	/*! Technology of the endpoint */
	const char *tech;
	/*! ID of the endpoint */
	const char *resource;
};
/*!
 * \brief Details for an endpoint.
 *
 * \param headers HTTP headers
 * \param args Swagger parameters
 * \param[out] response HTTP response
 */
void ast_ari_endpoints_get(struct ast_variable *headers, struct ast_ari_endpoints_get_args *args, struct ast_ari_response *response);
/*! Argument struct for ast_ari_endpoints_send_message_to_endpoint() */
struct ast_ari_endpoints_send_message_to_endpoint_args {
	/*! Technology of the endpoint */
	const char *tech;
	/*! ID of the endpoint */
	const char *resource;
	/*! The endpoint resource or technology specific identity to send this message from. Valid resources are sip, pjsip, and xmpp. */
	const char *from;
	/*! The body of the message */
	const char *body;
	struct ast_json *variables;
};
/*!
 * \brief Body parsing function for /endpoints/{tech}/{resource}/sendMessage.
 * \param body The JSON body from which to parse parameters.
 * \param[out] args The args structure to parse into.
 * \retval zero on success
 * \retval non-zero on failure
 */
int ast_ari_endpoints_send_message_to_endpoint_parse_body(
	struct ast_json *body,
	struct ast_ari_endpoints_send_message_to_endpoint_args *args);

/*!
 * \brief Send a message to some endpoint in a technology.
 *
 * \param headers HTTP headers
 * \param args Swagger parameters
 * \param[out] response HTTP response
 */
void ast_ari_endpoints_send_message_to_endpoint(struct ast_variable *headers, struct ast_ari_endpoints_send_message_to_endpoint_args *args, struct ast_ari_response *response);

#endif /* _ASTERISK_RESOURCE_ENDPOINTS_H */
