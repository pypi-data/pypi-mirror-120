import math

import numpy as np

class SsdAnchorsCalculatorOptions:
	def __init__(self, input_size_width, input_size_height, min_scale, max_scale
		, num_layers, feature_map_width, feature_map_height
		, strides, aspect_ratios, anchor_offset_x=0.5, anchor_offset_y=0.5
		, reduce_boxes_in_lowest_layer=False, interpolated_scale_aspect_ratio=1.0
		, fixed_anchor_size=False):
		# Size of input images.
		self.input_size_width = input_size_width
		self.input_size_height = input_size_height
		# Min and max scales for generating anchor boxes on feature maps.
		self.min_scale = min_scale
		self.max_scale = max_scale
		# The offset for the center of anchors. The value is in the scale of stride.
		# E.g. 0.5 meaning 0.5 * |current_stride| in pixels.
		self.anchor_offset_x = anchor_offset_x
		self.anchor_offset_y = anchor_offset_y
		# Number of output feature maps to generate the anchors on.
		self.num_layers = num_layers
		# Sizes of output feature maps to create anchors. Either feature_map size or
		# stride should be provided.
		self.feature_map_width = feature_map_width
		self.feature_map_height = feature_map_height
		self.feature_map_width_size = len(feature_map_width)
		self.feature_map_height_size = len(feature_map_height)
		# Strides of each output feature maps.
		self.strides = strides
		self.strides_size = len(strides)
		# List of different aspect ratio to generate anchors.
		self.aspect_ratios = aspect_ratios
		self.aspect_ratios_size = len(aspect_ratios)
		# A boolean to indicate whether the fixed 3 boxes per location is used in the lowest layer.
		self.reduce_boxes_in_lowest_layer = reduce_boxes_in_lowest_layer
		# An additional anchor is added with this aspect ratio and a scale
		# interpolated between the scale for a layer and the scale for the next layer
		# (1.0 for the last layer). This anchor is not included if this value is 0.
		self.interpolated_scale_aspect_ratio = interpolated_scale_aspect_ratio
		# Whether use fixed width and height (e.g. both 1.0f) for each anchor.
		# This option can be used when the predicted anchor width and height are in  pixels.
		self.fixed_anchor_size = fixed_anchor_size
	def to_string(self):
		return 'input_size_width: {:}\ninput_size_height: {:}\nmin_scale: {:}\nmax_scale: {:}\nanchor_offset_x: {:}\nanchor_offset_y: {:}\nnum_layers: {:}\nfeature_map_width: {:}\nfeature_map_height: {:}\nstrides: {:}\naspect_ratios: {:}\nreduce_boxes_in_lowest_layer: {:}\ninterpolated_scale_aspect_ratio: {:}\nfixed_anchor_size: {:}'\
		.format(self.input_size_width, self.input_size_height, self.min_scale, self.max_scale
			, self.anchor_offset_x, self.anchor_offset_y, self.num_layers
			, self.feature_map_width, self.feature_map_height, self.strides, self.aspect_ratios
			, self.reduce_boxes_in_lowest_layer, self.interpolated_scale_aspect_ratio
			, self.fixed_anchor_size)

class Anchor:
	def __init__(self, x_center, y_center, h, w):
		self.x_center = x_center
		self.y_center = y_center
		self.h = h
		self.w = w
	def to_string(self):
		return 'x_center: {:}, y_center: {:}, h: {:}, w: {:}'.format(self.x_center, self.y_center, self.h, self.w)

"""
    Non-max Suppression Algorithm
    @param list  Object candidate bounding boxes
    @param list  Confidence score of bounding boxes
    @param float IoU threshold
    @return Rest boxes after nms operation
"""
def nms(bounding_boxes, confidence_score, threshold):
    # If no bounding boxes, return empty list
    if len(bounding_boxes) == 0:
        return [], []

    # Bounding boxes
    boxes = np.array(bounding_boxes)

    # coordinates of bounding boxes
    start_x = boxes[:, 0]
    start_y = boxes[:, 1]
    end_x = boxes[:, 2]
    end_y = boxes[:, 3]

    # Confidence scores of bounding boxes
    score = np.array(confidence_score)

    # Picked bounding boxes
    picked_boxes = []
    picked_score = []

    # Compute areas of bounding boxes
    areas = (end_x - start_x + 1) * (end_y - start_y + 1)

    # Sort by confidence score of bounding boxes
    order = np.argsort(score)

    # Iterate bounding boxes
    while order.size > 0:
        # The index of largest confidence score
        index = order[-1]

        # Pick the bounding box with largest confidence score
        picked_boxes.append(bounding_boxes[index])
        picked_score.append(confidence_score[index])

        # Compute ordinates of intersection-over-union(IOU)
        x1 = np.maximum(start_x[index], start_x[order[:-1]])
        x2 = np.minimum(end_x[index], end_x[order[:-1]])
        y1 = np.maximum(start_y[index], start_y[order[:-1]])
        y2 = np.minimum(end_y[index], end_y[order[:-1]])

        # Compute areas of intersection-over-union
        w = np.maximum(0.0, x2 - x1 + 1)
        h = np.maximum(0.0, y2 - y1 + 1)
        intersection = w * h

        # Compute the ratio between intersection and union
        ratio = intersection / (areas[index] + areas[order[:-1]] - intersection)

        left = np.where(ratio < threshold)
        order = order[left]

    return picked_boxes, picked_score


def gen_anchors(options):
	anchors = []
	# Verify the options.
	if (options.strides_size != options.num_layers):
		print("strides_size and num_layers must be equal.")
		return []

	layer_id = 0
	while (layer_id < options.strides_size):
		anchor_height = []
		anchor_width = []
		aspect_ratios = []
		scales = []

		# For same strides, we merge the anchors in the same order.
		last_same_stride_layer = layer_id
		while (last_same_stride_layer < options.strides_size and options.strides[last_same_stride_layer] == options.strides[layer_id]):
			scale = options.min_scale + (options.max_scale - options.min_scale) * 1.0 * last_same_stride_layer / (options.strides_size - 1.0)
			if (last_same_stride_layer == 0 and options.reduce_boxes_in_lowest_layer):
				# For first layer, it can be specified to use predefined anchors.
				aspect_ratios.append(1.0)
				aspect_ratios.append(2.0)
				aspect_ratios.append(0.5)
				scales.append(0.1)
				scales.append(scale)
				scales.append(scale)
			else:
				for aspect_ratio_id in range(options.aspect_ratios_size):
					aspect_ratios.append(options.aspect_ratios[aspect_ratio_id])
					scales.append(scale)
				
				if (options.interpolated_scale_aspect_ratio > 0.0):
					scale_next = 1.0 if last_same_stride_layer == options.strides_size - 1 else options.min_scale + (options.max_scale - options.min_scale) * 1.0 * (last_same_stride_layer+1) / (options.strides_size - 1.0)
					scales.append(math.sqrt(scale * scale_next))
					aspect_ratios.append(options.interpolated_scale_aspect_ratio)
			last_same_stride_layer += 1
		for i in range(len(aspect_ratios)):
			ratio_sqrts = math.sqrt(aspect_ratios[i])
			anchor_height.append(scales[i] / ratio_sqrts)
			anchor_width.append(scales[i] * ratio_sqrts)

		feature_map_height = 0
		feature_map_width = 0
		if (options.feature_map_height_size > 0):
			feature_map_height = options.feature_map_height[layer_id]
			feature_map_width = options.feature_map_width[layer_id]
		else:
			stride = options.strides[layer_id]
			feature_map_height = math.ceil(1.0 * options.input_size_height / stride)
			feature_map_width = math.ceil(1.0 * options.input_size_width / stride)

		for y in range(feature_map_height):
			for x in range(feature_map_width):
				for anchor_id in range(len(anchor_height)):
					# TODO: Support specifying anchor_offset_x, anchor_offset_y.
					x_center = (x + options.anchor_offset_x) * 1.0 / feature_map_width
					y_center = (y + options.anchor_offset_y) * 1.0 / feature_map_height
					w = 0
					h = 0
					if (options.fixed_anchor_size):
						w = 1.0
						h = 1.0
					else:
						w = anchor_width[anchor_id]
						h = anchor_height[anchor_id]
					new_anchor = Anchor(x_center, y_center, h, w)
					anchors.append(new_anchor)
		layer_id = last_same_stride_layer
	return anchors